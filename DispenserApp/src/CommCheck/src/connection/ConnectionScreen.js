import React from 'react'
import RNBluetoothClassic from 'react-native-bluetooth-classic'
// import {
//   Container,
//   Header,
//   Left,
//   Button,
//   Icon,
//   Body,
//   Title,
//   Subtitle,
//   Right,
// } from 'native-base';
import { Button } from 'react-native-ui-lib'
import {
  FlatList,
  View,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Text
} from 'react-native'
import { Buffer } from 'buffer'
import PushNotification from 'react-native-push-notification'
import { msgsFromDispenserTypes } from '../../../Config/constants'
import { timeIntervalForFeedbackReminder } from '../../../Config/constants'

/**
 * Manages a selected device connection.  The selected Device should
 * be provided as {@code props.device}, the device will be connected
 * to and processed as such.
 *
 * @author kendavidson
 */
export default class ConnectionScreen extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      amountText: undefined,
      podSerialText: undefined,
      podTypeText: undefined,
      data: [],
      polling: false,
      connection: false,
      connectionOptions: {
        DELIMITER: '9'
      }
    }
  }
  /**
   * Removes the current subscriptions and disconnects the specified
   * device.  It could be possible to maintain the connection across
   * the application, but for now the connection is within the context
   * of this screen.
   */
  async componentWillUnmount() {
    if (this.state.connection) {
      try {
        await this.props.device.disconnect()
      } catch (error) {
        // Unable to disconnect from device
      }
    }

    this.uninitializeRead()
  }

  /**
   * Attempts to connect to the provided device.  Once a connection is
   * made the screen will either start listening or polling for
   * data based on the configuration.
   */
  componentDidMount() {
    setTimeout(() => this.connect(), 0)
  }

  async connect() {
    try {
      let connection = await this.props.device.isConnected()
      if (!connection) {
        this.addData({
          data: `Attempting connection to ${this.props.device.address}`,
          timestamp: new Date(),
          type: 'error'
        })

        console.log(this.state.connectionOptions)
        connection = await this.props.device.connect()

        this.addData({
          data: 'Connection successful',
          timestamp: new Date(),
          type: 'info'
        })
      } else {
        this.addData({
          data: `Connected to ${this.props.device.address}`,
          timestamp: new Date(),
          type: 'error'
        })
      }

      this.setState({ connection })
      this.initializeRead()
    } catch (error) {
      this.addData({
        data: `Connection failed: ${error.message}`,
        timestamp: new Date(),
        type: 'error'
      })
    }
  }

  async disconnect(disconnected) {
    try {
      if (!disconnected) {
        disconnected = await this.props.device.disconnect()
      }

      this.addData({
        data: 'Disconnected',
        timestamp: new Date(),
        type: 'info'
      })

      this.setState({ connection: !disconnected })
    } catch (error) {
      this.addData({
        data: `Disconnect failed: ${error.message}`,
        timestamp: new Date(),
        type: 'error'
      })
    }

    // Clear the reads, so that they don't get duplicated
    this.uninitializeRead()
  }

  initializeRead() {
    this.disconnectSubscription = RNBluetoothClassic.onDeviceDisconnected(() =>
      this.disconnect(true)
    )
    console.log('heree')
    if (this.state.polling) {
      this.readInterval = setInterval(() => this.performRead(), 5000)
    } else {
      console.log('readinggg')
      this.readSubscription = this.props.device.onDataReceived((data) =>
        this.onReceivedData(data)
      )
    }
  }

  /**
   * Clear the reading functionality.
   */
  uninitializeRead() {
    if (this.readInterval) {
      clearInterval(this.readInterval)
    }
    if (this.readSubscription) {
      this.readSubscription.remove()
    }
  }

  async performRead() {
    try {
      console.log('Polling for available messages')
      let available = await this.props.device.available()
      console.log(`There is data available [${available}], attempting read`)

      if (available > 0) {
        for (let i = 0; i < available; i++) {
          console.log(`reading ${i}th time`)
          let data = await this.props.device.read()

          console.log(`Read data ${data}`)
          console.log(data)
          this.onReceivedData({ data })
        }
      }
    } catch (err) {
      console.log(err)
    }
  }

  /**
   * Handles the ReadEvent by adding a timestamp and applying it to
   * list of received data.
   *
   * @param {ReadEvent} event
   */
  async onReceivedData(event) {
    event.timestamp = new Date()
    this.addDataMessage({
      ...event,
      timestamp: new Date(),
      type: 'receive'
    })
  }

  async addData(message) {
    try {
      console.log('message received: ' + JSON.stringify(message))
      const parsedAns = JSON.parse(message.data)
      console.log(parsedAns.podType)
      this.setState({ data: [message, ...this.state.data] })
    } catch (e) {
      console.log('')
    }
  }

  getUserTime(date) {
    const tzoffset = date.getTimezoneOffset() * 60000 //offset in milliseconds
    return new Date(Date.now() - tzoffset).toISOString().slice(0, -1)
  }

  async doseRequests(podSerial, podType, amount) {
    const { controller } = this.props
    try {
      await controller.registerPod(podSerial, podType)
      const dosingTime = this.getUserTime(new Date())
      await controller.dose(podSerial, parseFloat(amount), dosingTime)
    } catch (e) {
      console.log(e)
    }
  }
  setFeedbackReminderTime = (dosingTime) => {
    let dosingTimeObj = new Date(dosingTime)
    dosingTimeObj.setHours(
      dosingTimeObj.getHours() + timeIntervalForFeedbackReminder
    )
    console.log('the feedback reminder will be at:', dosingTimeObj)
    return dosingTimeObj
  }

  async addDataMessage(message) {
    try {
      console.log('message received: ' + JSON.stringify(message))
      console.log(message.data.substring(message.data.indexOf('{')))
      const messageObj = message.data.substring(message.data.indexOf('{'))
      const messageContent = JSON.parse(messageObj)
      const localTime = this.getUserTime(new Date(message.timestamp))
      console.log(localTime)
      const timeToRemindFeedBack = this.setFeedbackReminderTime(localTime)
      await this.doseRequests(
        messageContent.podSerial,
        messageContent.podType,
        messageContent.amount
      )
      if (messageContent.type === msgsFromDispenserTypes.DOSING) {
        console.log(message.timestamp)
        PushNotification.localNotification({
          channelId: this.props.consumer.email || 'gilgu@gmail.com',
          title: `Message from dispneser ${this.props.device.name}`,
          message: `Dose has been made:\n  time: ${localTime.toString()} \n pod type: ${
            messageContent.podType
          }\n dosage:${messageContent.amount} mg` // (required)
        })
        PushNotification.localNotificationSchedule({
          channelId: this.props.consumer.email || 'gilgu@gmail.com',
          date: timeToRemindFeedBack,
          title: `Reminder For Feeback`,
          message: `This is reminder for dose feedback that has been made in: ${this.props.device.name}:\n  time: ${message.timestamp} \n pod type: ${messageContent.podType}\n dosage:${messageContent.amount} mg` // (required)
        })
      } else {
        PushNotification.localNotification({
          channelId: this.props.consumer.email || 'gilgu@gmail.com',
          title: `Message from dispneser ${this.props.device.name}`,
          message: `Pod  ${messageContent.podSerial} from type ${messageContent.podType} is running low` // (required)
        })
      }
    } catch (e) {
      console.log(e)
    }
    this.setState({ data: [message, ...this.state.data] })
  }

  async toggleConnection() {
    if (this.state.connection) {
      this.disconnect()
    } else {
      this.connect()
    }
  }

  /**
   * Attempts to send data to the connected Device.  The input text is
   * padded with a NEWLINE (which is required for most commands)
   */
  async sendData(type) {
    try {
      const messageToSend = `{"type":"${type}", "amount":"${this.state.amountText}", "podSerial":"${this.state.podSerialText}", "podType":"${this.state.podTypeText}"}`
      console.log(`Attempting to send data ${messageToSend}`)
      let message = messageToSend + '\n'
      await RNBluetoothClassic.writeToDevice(this.props.device.address, message)
      console.log('---wrote 1')

      this.addData({
        timestamp: new Date(),
        data: this.state.text,
        type: 'sent'
      })
      console.log('---added data')

      let data = Buffer.alloc(10, 0xef)
      await this.props.device.write(data)
      console.log('---wrote 2')

      this.addData({
        timestamp: new Date(),
        data: `Byte array: ${data.toString()}`,
        type: 'sent'
      })
      console.log('---added data 2')

      this.setState({ text: undefined })
    } catch (error) {
      console.log(error)
    }
  }

  render() {
    let toggleIcon = this.state.connection
      ? 'radio-button-on'
      : 'radio-button-off'
    // return <View><Text>Herro</Text></View>
    return (
      <View style={styles.container}>
        {/* <View style={styles.connectionScreenWrapper}>
          <FlatList
            style={styles.connectionScreenOutput}
            contentContainerStyle={{ justifyContent: 'flex-end' }}
            inverted
            ref="scannedDataList"
            data={this.state.data}
            keyExtractor={(item) => item.timestamp.toISOString()}
            renderItem={({ item }) => (
              <View
                id={item.timestamp.toISOString()}
                flexDirection={'row'}
                justifyContent={'flex-start'}
              >
                <Text>{item.timestamp.toLocaleDateString()}</Text>
                <Text>{item.type === 'sent' ? ' < ' : ' > '}</Text>
                <Text flexShrink={1}>{item.data.trim()}</Text>
              </View>
            )}
          /> */}
        <Text
          style={styles.header}
        >{`Hello ${this.props.consumer.firstName} You are connected to dispneser: ${this.props.device.name}`}</Text>
        <View style={styles.option}>
          <TextInput
            style={styles.inputAreaTextInput}
            placeholder={'Enter amount to dispense'}
            value={this.state.amountText}
            onChangeText={(text) => this.setState({ amountText: text })}
            autoCapitalize="none"
            autoCorrect={false}
            returnKeyType="send"
            keyboardType="numeric"
          />
        </View>

        <View style={styles.option}>
          <TextInput
            style={styles.inputAreaTextInput}
            placeholder={'Enter pod serial num'}
            value={this.state.podSerialText}
            onChangeText={(text) => this.setState({ podSerialText: text })}
            autoCapitalize="none"
            autoCorrect={false}
            returnKeyType="send"
          />
        </View>
        <View style={styles.option}>
          <TextInput
            style={styles.inputAreaTextInput}
            placeholder={'Enter pod typer'}
            value={this.state.podTypeText}
            onChangeText={(text) => this.setState({ podTypeText: text })}
            autoCapitalize="none"
            autoCorrect={false}
            returnKeyType="send"
          />
        </View>
        <View style={styles.option}>
          <Button
            backgroundColor="green"
            label="Dose"
            borderRadius={7}
            onPress={() => this.sendData(msgsFromDispenserTypes.DOSING)}
          />
          <Button
            backgroundColor="green"
            label="Alert pod running low"
            borderRadius={7}
            onPress={() =>
              this.sendData(msgsFromDispenserTypes.POD_RUNNING_LOW)
            }
          />
        </View>
      </View>
    )
  }
}

const InputArea = ({ text, onChangeText, onSend, disabled }) => {
  let style = disabled ? styles.inputArea : styles.inputAreaConnected
  return (
    <View style={style}>
      <TextInput
        style={styles.inputAreaTextInput}
        placeholder={'Command/Text'}
        value={text}
        onChangeText={onChangeText}
        autoCapitalize="none"
        autoCorrect={false}
        onSubmitEditing={onSend}
        returnKeyType="send"
        disabled={disabled}
      />
      <TouchableOpacity
        style={styles.inputAreaSendButton}
        onPress={onSend}
        disabled={disabled}
      >
        <Text>Send</Text>
      </TouchableOpacity>
    </View>
  )
}

/**
 * TextInput and Button for sending
 */
const styles = StyleSheet.create({
  submitBtn: {
    marginTop: 10,
    paddingTop: 10,
    paddingBottom: 10,
    backgroundColor: 'gray',
    borderRadius: 10,
    borderWidth: 1,
    textAlign: 'center',
    borderColor: '#fff',
    alignContent: 'center'
  },
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    padding: 35,
    backgroundColor: '#fff'
  },
  header: {
    fontSize: 30,
    alignContent: 'flex-start',
    marginBottom: 40
  },
  option: {
    display: 'flex',
    flexDirection: 'row-reverse',
    right: 10,
    width: '100%',
    justifyContent: 'space-between',
    marginBottom: 15,
    paddingBottom: 15,
    alignSelf: 'center',
    borderColor: '#ccc',
    borderBottomWidth: 1
  },
  connectionScreenWrapper: {
    flex: 1
  },
  connectionScreenOutput: {
    flex: 1,
    paddingHorizontal: 8
  },
  inputArea: {
    flexDirection: 'row',
    alignContent: 'stretch',
    backgroundColor: '#ccc',
    paddingHorizontal: 16,
    paddingVertical: 6
  },
  inputAreaConnected: {
    flexDirection: 'row',
    alignContent: 'stretch',
    backgroundColor: '#90EE90',
    paddingHorizontal: 16,
    paddingVertical: 6
  },
  inputAreaTextInput: {
    flex: 1,
    height: 40
  },
  inputAreaSendButton: {
    justifyContent: 'center',
    flexShrink: 1
  }
})
