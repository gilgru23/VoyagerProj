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

export default function Bluetooth({ navigation, route }) {
  const [bondedDevices, setBondedDevices] = useState([])
  const [selctedDevice, setSelectedDevice] = useState()
  const [controller, setConroller] = useState(route.params.controller)

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

  const registerDevice = async (selectedDevice) => {
    await controller.registerDispenser(selectedDevice.id, selctedDevice.name)
    if (response.status === responseStatus.SUCCESS) {
      navigation.navigate('PersonalPage', {
        consumer: route.params.consumer,
        device: response.content
      })
    } else {
      alert(response.content)
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
          onPress={() => registerDevice(selctedDevice)}
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
