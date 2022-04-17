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

export default function PersonalPods({ route, navigation }) {
  const [pods, setPods] = useState([])
  useEffect(() => {
    console.log(getPodsPerDispenser(route.params.device.id))
    setPods(getPodsPerDispenser(route.params.device.id))
  }, [])

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Image source={require('./assets/voyagerLogo.png')} />
        <Text>{`The pods that are connected to the dispenser:${route.params.device.name}`}</Text>
      </View>
      {pods.map((pod) => (
        <TouchableOpacity
          style={styles.submitBtn}
          onPress={() =>
            navigation.navigate('Current Pod', {
              pod: pod
            })
          }
        >
          <Text style={{ color: 'white' }}>{pod}</Text>
        </TouchableOpacity>
      ))}
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'flex-end'
  },
  menu: {
    marginRight: 10
  },

  header: {
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20
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
