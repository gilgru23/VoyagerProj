import React, { useState } from 'react'
import RNBluetoothClassic, {
  BluetoothDevice
} from 'react-native-bluetooth-classic'
import {
  StyleSheet,
  Text,
  View,
  Image,
  TextInput,
  Button,
  TouchableOpacity,
  PermissionsAndroid
} from 'react-native'
import { Buffer } from 'buffer'

export default function Communication({ navigation, device, route }) {
  const [dataToSend, setDataSend] = useState('')
  const [controller, setConroller] = useState(route.params.controller)

  const sendData = async () => {
    try {
      await RNBluetoothClassic.writeToDevice(device.address, dataToSend)

      console.log({
        timestamp: new Date(),
        data: dataToSend,
        type: 'sent'
      })

      let data = Buffer.alloc(10, 0xef)
      await device.write(dataToSend)

      console.log({
        timestamp: new Date(),
        data: `Byte array: ${dataToSend.toString()}`,
        type: 'sent'
      })
    } catch (error) {
      console.log(error)
    }
  }

  const performRead = async () => {
    while (true) {
      try {
        console.log('Polling for available messages')
        let available = await device.available()
        console.log(`There is data available [${available}], attempting read`)

        if (available > 0) {
          for (let i = 0; i < available; i++) {
            console.log(`reading ${i}th time`)
            let data = await device.read()

            console.log(`Read data ${data}`)
            console.log(data)
          }
        }
      } catch (err) {
        console.log(err)
      }
    }
  }

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.inputStyle}
        placeholder="Send data"
        value={dataToSend}
        onChangeText={(val) => this.setDataSend(val)}
      />
      <Button title="Send Data" onPress={() => sendData()} />
      <Button title="Get Data" onPress={() => performRead()} />
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    marginTop: '10%',
    alignItems: 'center'
  },

  image: {},

  dispenserImg: {
    height: '50%',
    width: '50%'
  },

  inputView: {
    backgroundColor: '#eee',
    borderRadius: 30,
    width: '70%',
    height: 45,
    marginBottom: 20,

    alignItems: 'center'
  },

  TextInput: {
    height: 50,
    flex: 1,
    padding: 10,
    marginLeft: 20
  },

  connection_button: {
    height: 30,
    marginBottom: 30
  },

  buttonLayout: {
    display: 'flex',
    flexDirection: 'row'
  },

  loginBtn: {
    width: '50%',
    borderRadius: 25,
    height: 50,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 40,
    backgroundColor: '#eee'
  }
})
