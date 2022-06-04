import React from 'react'
import { Platform, Image } from 'react-native'
import RNBluetoothClassic from 'react-native-bluetooth-classic'
import { PermissionsAndroid, FlatList, StyleSheet, Text } from 'react-native'
import { Colors, TouchableOpacity, View, ListItem } from 'react-native-ui-lib'
import { responseStatus } from '../../../Config/constants'

/**
 * See https://reactnative.dev/docs/permissionsandroid for more information
 * on why this is required (dangerous permissions).
 */
const requestAccessFineLocationPermission = async () => {
  const granted = await PermissionsAndroid.request(
    PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT,
    {
      title: 'Access fine location required for discovery',
      message:
        'In order to perform discovery, you must enable/allow ' +
        'fine location access.',
      buttonNeutral: 'Ask Me Later',
      buttonNegative: 'Cancel',
      buttonPositive: 'OK'
    }
  )
  return granted === PermissionsAndroid.RESULTS.GRANTED
}

/**
 * Displays the device list and manages user interaction.  Initially
 * the NativeDevice[] contains a list of the bonded devices.  By using
 * the Discover Devices action the list will be updated with unpaired
 * devices.
 *
 * From here:
 * - unpaired devices can be paired
 * - paired devices can be connected
 *
 * @author kendavidson
 */
export default class DeviceListScreen extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      registerdDevices: [],
      devices: [],
      accepting: false,
      discovering: false,
      msg: ''
    }
  }

  async componentDidMount() {
    await requestAccessFineLocationPermission()
    const response = await this.props.controller.getDispenserOfConsumer()
    if ((response.status = responseStatus.SUCCESS)) {
      this.setState({ registerdDevices: response.content })
    }
    this.getBondedDevices()
  }

  componentWillUnmount() {
    if (this.state.accepting) {
      this.cancelAcceptConnections(false)
    }

    if (this.state.discovering) {
      this.cancelDiscovery(false)
    }
  }

  /**
   * Gets the currently bonded devices.
   */
  getBondedDevices = async (unloading) => {
    console.log('DeviceListScreen::getBondedDevices')
    try {
      let bonded = await RNBluetoothClassic.getBondedDevices()
      console.log('DeviceListScreen::getBondedDevices found', bonded)

      if (!unloading) {
        this.setState({ devices: bonded })
      }
    } catch (error) {
      this.setState({ devices: [] })
      this.display(err.message)
    }
  }

  /**
   * Starts attempting to accept a connection.  If a device was accepted it will
   * be passed to the application context as the current device.
   */
  acceptConnections = async () => {
    if (this.state.accepting) {
      this.display('Already accepting connections')
      return
    }

    this.setState({ accepting: true })

    try {
      let device = await RNBluetoothClassic.accept({ delimiter: '\n' })
      if (device) {
        this.display('device accepted!')
        console.log('device accepted')
        this.props.selectDevice(device, true)
      }
    } catch (error) {
      // If we're not in an accepting state, then chances are we actually
      // requested the cancellation.  This could be managed on the native
      // side but for now this gives more options.
      if (!this.state.accepting) {
        this.display('Attempt to accept connection failed.')
      } else {
        this.display('unknown failure in accepting connection')
      }
    } finally {
      this.setState({ accepting: false })
    }
  }

  /**
   * Cancels the current accept - might be wise to check accepting state prior
   * to attempting.
   */
  cancelAcceptConnections = async () => {
    if (!this.state.accepting) {
      return
    }

    try {
      let cancelled = await RNBluetoothClassic.cancelAccept()
      this.setState({ accepting: !cancelled })
    } catch (error) {
      this.display('Unable to cancel accept connection')
    }
  }

  printDevices = (ds) => {
    console.log('num devices = ' + ds.length)
    ds.forEach((d) => {
      console.log('\n' + d.name)
      console.log(JSON.stringify(d) + '\n\n')
    })
  }

  display = (msg) => {
    console.log(msg)
    this.setState({ msg })
  }

  startDiscovery = async () => {
    console.log('starting discovery')
    try {
      let granted = await requestAccessFineLocationPermission()

      if (!granted) {
        throw new Error('Access fine location was not granted')
      }

      this.setState({ discovering: true })

      let devices = [...this.state.devices]

      try {
        let unpaired = await RNBluetoothClassic.startDiscovery()

        let unbonded = unpaired.filter((d) => !d.bonded)
        // this.printDevices(unbonded)

        let index = devices.findIndex((d) => !d.bonded)
        if (index >= 0) {
          devices.splice(index, devices.length - index, ...unpaired)
        } else {
          devices.push(...unpaired)
        }
        // devices = unbonded;
        this.display(`Found ${unpaired.length} unpaired devices.`)
      } finally {
        this.display('discovery succeeded!')
        this.setState({ devices, discovering: false })
      }
    } catch (err) {
      this.display('discovery failed :( \n' + err.message)
    }
  }

  cancelDiscovery = async () => {
    try {
    } catch (error) {
      this.display('Error occurred while attempting to cancel discover devices')
    }
  }

  requestEnabled = async () => {
    try {
    } catch (error) {
      this.display(`Error occurred while enabling bluetooth: ${error.message}`)
    }
  }

  isDeviceOfInterest = (d) => {
    const lcName = d.name.toLowerCase()
    console.log(d.name)
    return (
      lcName.includes('red') ||
      lcName.includes('gal') ||
      lcName.includes('lg') ||
      lcName.includes('plt') ||
      lcName.includes('21')
    )
  }

  render() {
    let toggleAccept = this.state.accepting
      ? () => this.cancelAcceptConnections()
      : () => this.acceptConnections()
    let toggleDiscovery = this.state.discovering
      ? () => this.cancelDiscovery()
      : () => this.startDiscovery()
    const acceptTxt = this.state.accepting
      ? 'Accepting (cancel)...'
      : 'Accept Connection'
    const discoveringTxt = this.state.discovering
      ? 'Discovering (cancel)... '
      : 'Discover Devices'

    const registerdDevicesToDisplay = this.state.devices.filter((d) => {
      try {
        return this.state.registerdDevices.some(
          (registerdDevice) => registerdDevice.id === d.address
        )
      } catch (e) {
        console.log(e)
      }
    })
    const unRegisterdDevicesToDisplay = this.state.devices.filter((d) => {
      try {
        return (
          !this.state.registerdDevices.some(
            (registerdDevice) => registerdDevice.id === d.address
          ) && this.isDeviceOfInterest(d)
        )
      } catch (e) {
        console.log(e)
      }
    })
    return (
      <View>
        <Text text50 marginL-s5 marginV-s3 style={styles.title}>
          Connect to dispenser
        </Text>
        <Text>{this.state.msg}</Text>
        {this.props.bluetoothEnabled ? (
          <>
            {Platform.OS !== 'ios' ? (
              <View>
                <TouchableOpacity block onPress={toggleAccept}>
                  <Text> {acceptTxt} </Text>
                </TouchableOpacity>
              </View>
            ) : undefined}

            <View>
              <Text text50 marginL-s5 marginV-s3 style={styles.subTitle}>
                Available and registered devices
              </Text>
              <DeviceList
                devices={registerdDevicesToDisplay}
                onPress={this.props.selectDevice}
                registered={true}
              />
              <Text text50 marginL-s5 marginV-s3 style={styles.subTitle}>
                Available and unrregistered devices
              </Text>
              <DeviceList
                devices={unRegisterdDevicesToDisplay}
                onPress={this.props.selectDevice}
                registered={false}
              />
            </View>
          </>
        ) : (
          <View>
            <Text>Bluetooth is OFF</Text>
            <TouchableOpacity onPress={() => this.requestEnabled()}>
              <Text>Enable Bluetooth</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
    )
  }
}

/**
 * Displays a list of Bluetooth devices.
 *
 * @param {NativeDevice[]} devices
 * @param {function} onPress
 * @param {function} onLongPress
 */
export const DeviceList = ({ devices, onPress, onLongPress, registered }) => {
  const renderItem = ({ item }) => {
    return (
      <DeviceListItem
        device={item}
        onPress={onPress}
        onLongPress={onLongPress}
        registered={registered}
      />
    )
  }

  return (
    <View>
      <FlatList
        data={devices}
        renderItem={renderItem}
        keyExtractor={(item) => item.address}
      />
    </View>
  )
}

export const DeviceListItem = ({
  device,
  onPress,
  onLongPress,
  registered
}) => {
  let bgColor = device.connected ? '#0f0' : '#fff'
  let icon = device.bonded ? 'ios-bluetooth' : 'ios-cellular'

  return (
    <TouchableOpacity
      activeOpacity={1}
      bg-blue40
      paddingH-s5
      paddingV-s4
      key={device.address}
      activeBackgroundColor={Colors.blue20}
      style={{
        borderBottomWidth: 1,
        borderColor: Colors.white,
        textAlign: 'left'
      }}
      onPress={() => onPress(device, registered)}
      onLongPress={() => onLongPress(device)}
    >
      <View style={styles.card}>
        <Text white text70M style={styles.option}>
          {device.name}
        </Text>
        <Image
          source={require('../assets/dispenser.png')}
          style={styles.image}
        />
        {/* <Text white text70M style={styles.option}>
          {device.address}
        </Text> */}
      </View>
    </TouchableOpacity>
  )
}

const styles = StyleSheet.create({
  deviceListItem: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
    paddingHorizontal: 8,
    paddingVertical: 8
  },
  deviceListItemIcon: {
    paddingHorizontal: 16,
    paddingVertical: 8
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
  },
  container: {
    textAlign: 'center'
  },
  subTitle: {
    fontSize: 15,
    marginBottom: 10,
    textAlign: 'center',
    fontWeight: 'bold'
  },
  title: {
    fontSize: 25,
    marginBottom: 10,
    textAlign: 'center',
    fontWeight: 'bold'
  },

  option: {
    color: 'white',
    alignContent: 'flex-start'
  },
  image: {
    width: 20,
    height: 40,
    marginLeft: 'auto'
  },
  card: {
    display: 'flex',
    flexDirection: 'row-reverse',
    alignItems: 'flex-start',
    alignContent: 'space-between'
  }
})
