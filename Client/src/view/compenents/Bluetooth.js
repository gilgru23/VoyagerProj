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

export default function Bluetooth({ navigation }) {
  const [bondedDevices, setBondedDevices] = useState([])

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
      console.log(pairedDevices)
    } catch (err) {
      console.log(err)
    }
  }

  return (
    <View style={styles.container}>
      {/* <Image source={require("../../../assets/voyagerLogo.png")} /> */}
      {/* <Image style={styles.image} source={require("./assets/voyagerLogo.png")} /> */}
      {/* <Image style={styles.dispenserImg} source={require("./assets/dispenser.png")} /> */}
      <Button title="Show bonded Dispensers" onPress={() => bluetoothScan()} />
      <Text>Bonded Devices List:</Text>
      {bondedDevices.map((device) => (
        <Button
          title={device.name}
          onPress={() => connect(device)}
          style={{ marginBottom: '20%' }}
        />
      ))}
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
