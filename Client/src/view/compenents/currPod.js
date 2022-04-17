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
import { getPodsPerDispenser } from '../../controller/controller'

export default function CurrPod({ route }) {
  const [pod, setPod] = useState('')
  useEffect(() => {
    console.log(route.params.pod)
    setPod(getPodsPerDispenser(route.params.pod))
  }, [])

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Image source={require('./assets/pod.png')} />
        <Text>{`Current pod is :${route.params.pod}`}</Text>
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    display: 'flex'
  },
  menu: {
    marginRight: 10
  },

  header: {
    alignItems: 'center',
    marginBottom: 20,
    fontSize: 20
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

  submitBtn: {
    marginTop: 10,
    paddingTop: 10,
    paddingBottom: 10,
    backgroundColor: 'gray',
    borderRadius: 10,
    borderWidth: 1,
    textAlign: 'center',
    borderColor: '#fff'
  }
})
