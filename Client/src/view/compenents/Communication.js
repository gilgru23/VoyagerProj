import React, { useState, useEffect } from 'react'
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

export default function Communication({ navigation, route }) {
  const [dataToSend, setDataSend] = useState('')
  const [connectedDevice, setConnectedDevice] = useState()
  const [controller, setConroller] = useState(route.params.controller)

  async function getConnections() {
    try {
      const connectedDevice = await RNBluetoothClassic.getConnectedDevices()
      console.log(connectedDevice)
      if (connectedDevice.length > 0) setConnectedDevice(connectedDevice[0])
    } catch (e) {
      console.log(e)
    }
  }
  acceptConnections = async () => {
    try {
      let device = await RNBluetoothClassic.accept({ delimiter: '\n' })
      if (device) {
        setConnectedDevice(device)
        // setConnectedDevice(device)
      }
    } catch (error) {
      console.log(error)
    }
  }
  const sendData = async () => {
    try {
      let message = dataToSend + '\n'
      await RNBluetoothClassic.writeToDevice(connectedDevice.address, message)
      console.log('---wrote 1')
      let data = Buffer.alloc(10, 0xef)
      await connectedDevice.write(data)
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <View style={styles.container}>
      {connectedDevice ? (
        <Text>{`You are connected to ${connectedDevice.name}`}</Text>
      ) : null}
      <TextInput
        style={styles.inputStyle}
        placeholder="Send data"
        value={dataToSend}
        onChangeText={(val) => setDataSend(val)}
      />
      <Button
        title="Accept connections"
        onPress={async () => await acceptConnections()}
      />
      <Button title="Send Data" onPress={() => sendData()} />
      <Button title="Get Data" onPress={() => performRead()} />
      <Button
        title="Get connection devices"
        onPress={async () => await getConnections()}
      />
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
