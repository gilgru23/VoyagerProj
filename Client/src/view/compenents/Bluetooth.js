import React, { useState } from 'react'
// import { registerDispenser } from '../../controller/controller'
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
import { Dispenser } from '../../model/dispenser'

export default function Bluetooth({ navigation, route }) {
  const [bondedDevices, setBondedDevices] = useState([])
  const [selctedDevice, setSelectedDevice] = useState()
  const [controller, setConroller] = useState(route.params.controller)
  const [connectedDevice, setConnectedDevice] = useState()
  const [polling, setPolling] = useState(false)
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

  const onReceivedData = (event) => {
    event.timestamp = new Date()
    console.log(event)
  }

  const initializeRead = (device) => {
    if (polling) {
      const readInterval = setInterval(() => this.performRead(), 5000)
    } else {
      const readSubscription = device.onDataReceived((data) =>
        onReceivedData(data)
      )
      // console.log(readSubscription)
    }
  }
  const connect = async (device) => {
    try {
      let connection = await device.isConnected()
      if (!connection) {
        connection = await device.connect()
      } else {
        const connectedDevices = await RNBluetoothClassic.getConnectedDevices()
        console.log(connectedDevices)
        connectedDevices.forEach((deviceConnectedBefore) => {
          if (device.address === deviceConnectedBefore.address) {
            setConnectedDevice(deviceConnectedBefore)
          }
          initializeRead(device)
        })
      }
      // this.initializeRead();
    } catch (error) {
      console.log(error)
    }
  }
  const registerDevice = async (selectedDevice) => {
    // await controller.registerDispenser(selectedDevice.id, selctedDevice.name)
    // if (response.status === responseStatus.SUCCESS) {
    //   navigation.navigate('PersonalPage', {
    //     consumer: route.params.consumer,
    //     device: response.content
    //   })
    // } else {
    //   alert('Error', response.content)
    // }
    navigation.navigate('PersonalPage', {
      consumer: route.params.consumer,
      device: new Dispenser(selectedDevice.id, selectedDevice.name)
    })
  }

  const bluetoothScan = async () => {
    await requestAccessFineLocationPermission()
    try {
      const devices = await RNBluetoothClassic.getBondedDevices({
        delimiter: '\r'
      })
      setBondedDevices(devices)
      // const pairedDevices = await RNBluetoothClassic.getConnectedDevices();
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
      {connectedDevice ? (
        <Text>{`You are already connected to ${connectedDevice.name}`}</Text>
      ) : null}
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
          onPress={() => connect(selctedDevice)}
        >
          <Text style={{ color: 'white' }}>
            {`connect to ${selctedDevice.name}`}
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
