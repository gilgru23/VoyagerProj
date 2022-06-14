// components/signup.js
import React, { useState, useEffect } from 'react'
import { ResourceIds as ids } from './ResourceIds'

import {
  StyleSheet,
  Text,
  View,
  TextInput,
  Button,
  Alert,
  ActivityIndicator,
  Image
} from 'react-native'
import { Picker } from '@react-native-picker/picker'
// import { registerUser } from '../../controller/controller'
import { responseStatus } from '../../Config/constants'
import { alert } from './utils'
import DateTimePicker from '@react-native-community/datetimepicker'
import PushNotification from 'react-native-push-notification'
import { toDateString } from '../../utilsFunctions'

export default function Signup({ navigation, route }) {
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('')
  const [dateModalOpen, setDateModalOpen] = useState(false)
  const [birthDate, setBirthDate] = useState(new Date())
  const [controller, setConroller] = useState(route.params.controller)

  async function register() {
    const response = await controller.registerUser(
      email,
      password,
      firstName,
      lastName,
      toDateString(birthDate)
    )
    console.log(responseStatus.SUCCESS)
    if (response.status === responseStatus.SUCCESS) {
      const responseLogin = await controller.loginUser(email, password)
      if (responseLogin.status === responseStatus.SUCCESS) {
        console.log('email for notification', email)
        createChannel(email)
        navigation.navigate('PersonalInfo', {
          firstName: firstName,
          lastName: lastName,
          email: email,
          birthDate: toDateString(birthDate)
        })
      } else {
        alert('Error', response.content)
      }
    } else {
      alert('Error', response.content)
    }
  }

  const createChannel = (consumerId) =>
    PushNotification.createChannel(
      {
        channelId: consumerId, // (required)
        channelName: 'Test channe', // (required)
        channelDescription: 'A channel to categorise your notifications', // (optional) default: undefined.
        playSound: false, // (optional) default: true
        soundName: 'default', // (optional) See `soundName` parameter of `localNotification` function
        vibrate: true // (optional) default: true. Creates the default vibration pattern if true.
      },
      (created) => console.log(`createChannel returned '${created}'`) // (optional) callback returns whether the channel was created, false means it already existed.
    )

  const onChangeDatePicker = (event, selectedDate) => {
    setBirthDate(selectedDate)
    setDateModalOpen(false)
  }

  return (
    <View style={styles.container}>
      <Image source={require('./assets/voyagerLogo.png')} marginLeft={50} />
      <TextInput
        style={styles.inputStyle}
        placeholder="First Name"
        value={firstName}
        onChangeText={(val) => setFirstName(val)}
        testID={ids.reg_firstName_et}
      />
      <TextInput
        style={styles.inputStyle}
        placeholder="Last Name"
        value={lastName}
        onChangeText={(val) => setLastName(val)}
        testID={ids.reg_lastName_et}
      />
      <TextInput
        style={styles.inputStyle}
        placeholder="Email"
        value={email}
        onChangeText={(val) => setEmail(val)}
        testID={ids.reg_email_et}
      />
      <TextInput
        style={styles.inputStyle}
        placeholder="Password"
        value={password}
        onChangeText={(val) => setPassword(val)}
        maxLength={15}
        secureTextEntry={true}
        testID={ids.reg_password_et}
      />
      <View style={styles.inputStyle}>
        <Text>Enter your Year Of Birth</Text>
        <Button
          onPress={() => setDateModalOpen(true)}
          title={birthDate.toDateString()}
          testID={ids.reg_dob_btn}
        />
      </View>
      {dateModalOpen && (
        <DateTimePicker
          testID="dateTimePicker"
          value={birthDate}
          mode={'date'}
          onChange={(event, selectedDate) =>
            onChangeDatePicker(event, selectedDate)
          }
        />
      )}
      {/* <Picker
          selectedValue={this.state.role}
          onValueChange={(itemValue, itemIndex) =>
            this.setState({ role: itemValue })
          }
          style={styles.inputStyle}
        >
          <Picker.Item label="Consumer" value="Consumer" />
          <Picker.Item label="Voyager Manager" value="Voyager Manager" />
          <Picker.Item label="Care Giver" value="Care Giver" />
        </Picker> */}

      <Button
        color="#3740FE"
        title="Signup"
        onPress={() => register()}
        testID={ids.reg_submit_btn}
      />
      <Text
        style={styles.loginText}
        onPress={() => navigation.navigate('Login')}
      >
        Already Registered? Click here to login
      </Text>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    padding: 35,
    backgroundColor: '#fff'
  },
  inputStyle: {
    width: '100%',
    marginBottom: 15,
    paddingBottom: 15,
    alignSelf: 'center',
    borderColor: '#ccc',
    borderBottomWidth: 1
  },
  loginText: {
    color: '#3740FE',
    marginTop: 25,
    textAlign: 'center'
  },
  preloader: {
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    position: 'absolute',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff'
  }
})
