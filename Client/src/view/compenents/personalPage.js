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

export default function PersonalPage({ route, navigation }) {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Image source={require('./assets/voyagerLogo.png')} />
        <Text>{`Hello ${route.params.consumer.firstName} you are connected to the dispenser:${route.params.device.name}`}</Text>
      </View>
      <Text>Explore:</Text>
      <View style={styles.menu}>
        <TouchableOpacity
          style={styles.submitBtn}
          onPress={() =>
            navigation.navigate('PersonalPods', {
              device: route.params.device
            })
          }
        >
          <Text style={{ color: 'white' }}>{`Personal pods page`}</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.submitBtn}
          onPress={() =>
            navigation.navigate('RegisterPod', {
              device: route.params.device
            })
          }
        >
          <Text style={{ color: 'white' }}>{`Register pod`}</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.submitBtn}
          onPress={() =>
            navigation.navigate('RecommendationPage', {
              device: route.params.device
            })
          }
        >
          <Text style={{ color: 'white' }}>{`Recommendation Page`}</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.submitBtn}
          onPress={() =>
            navigation.navigate('TrackingPage', {
              device: route.params.device
            })
          }
        >
          <Text style={{ color: 'white' }}>{`Track Usage Page`}</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.submitBtn}
          onPress={() =>
            navigation.navigate('Scheduler', {
              consumerId: route.params.consumer.email
            })
          }
        >
          <Text style={{ color: 'white' }}>{`Schedule Page`}</Text>
        </TouchableOpacity>
      </View>
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
