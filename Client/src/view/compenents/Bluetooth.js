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

export default function Bluetooth({ navigation, route }) {
  const [bondedDevices, setBondedDevices] = useState([])
  const [selctedDevice, setSelectedDevice] = useState()

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

  const connect = async (device) => {
    console.log(device)
    try {
      let connection = await device.isConnected()
      if (!connection) {
        console.log({
          data: `Attempting connection to ${device.address}`,
          timestamp: new Date(),
          type: 'error'
        })
        connection = await device.connect()

        console.log({
          data: 'Connection successful',
          timestamp: new Date(),
          type: 'info'
        })
      } else {
        console.log({
          data: `Connected to ${device.address}`,
          timestamp: new Date(),
          type: 'error'
        })
      }

      navigation.navigate('Communication', {
        device: device
      })
    } catch (error) {
      console.log({
        data: `Connection failed: ${error.message}`,
        timestamp: new Date(),
        type: 'error'
      })
    }
  }

  const bluetoothScan = async () => {
    await requestAccessFineLocationPermission()
    try {
      const devices = await RNBluetoothClassic.getBondedDevices({
        delimiter: '\r'
      })
      setBondedDevices(devices)
      // const pairedDevices = await RNBluetoothClassic.getConnectedDevices();
      console.log(devices)
    } catch (err) {
      console.log(err)
    }
  }

  return (
    <View style={styles.container}>
      <Image
        style={styles.dispenserImg}
        source={require('./assets/dispenser.png')}
      />
      <Button title="Show bonded Dispensers" onPress={() => bluetoothScan()} />
      <Text>Bonded Devices List:</Text>
      {bondedDevices.map((device) => (
        <TouchableOpacity
          style={styles.deviceBtn}
          onPress={() => setSelectedDevice(device)}
        >
          <Text style={{ color: 'white' }}>{device.name}</Text>
        </TouchableOpacity>
      ))}
      {selctedDevice ? (
        <TouchableOpacity
          style={styles.submitBtn}
          onPress={() => (
            console.log(route.params),
            navigation.navigate('PersonalPage', {
              consumer: route.params.consumer,
              device: { name: selctedDevice.name, id: selctedDevice.id }
            })
          )}
        >
          <Text style={{ color: 'white' }}>
            {`move to your personal with the dispenser ${selctedDevice.name}`}
          </Text>
        </TouchableOpacity>
      ) : null}
    </View>
  )
}

const styles = StyleSheet.create({
  head: { height: 40, backgroundColor: '#f1f8ff' },
  text: { margin: 6 },
  container: {
    flex: 1,
    marginTop: '5%',
    alignItems: 'center',
    flexDirection: 'column'
  },

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

  deviceBtn: {
    marginRight: 40,
    marginLeft: 40,
    marginTop: 5,
    paddingTop: 5,
    paddingBottom: 10,
    backgroundColor: 'gray',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#fff'
  },

  submitBtn: {
    marginRight: 40,
    marginLeft: 40,
    marginTop: 10,
    paddingTop: 10,
    paddingBottom: 10,
    backgroundColor: '#1E6738',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#fff'
  }
})
