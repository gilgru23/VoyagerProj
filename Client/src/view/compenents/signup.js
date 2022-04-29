// components/signup.js
import React, { Component } from 'react'
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
import { registerUser } from '../../controller/controller'
import { responseStatus } from '../../Config/constants'
import { alert } from '../../utils'

export default class Signup extends Component {
  constructor() {
    super()
    this.state = {
      firstName: '',
      lastName: '',
      email: '',
      password: '',
      isLoading: false,
      role: 'Consumer'
    }
  }
  updateInputVal = (val, prop) => {
    const state = this.state
    state[prop] = val
    this.setState(state)
  }
  async register() {
    const { email, password, firstName, lastName } = this.state
    console.log(email)
    const response = await registerUser(email, password, firstName, lastName)
    console.log(responseStatus.SUCCESS)
    if (response.status === responseStatus.SUCCESS) {
      this.props.navigation.navigate('PersonalInfo', {
        firstName: this.state.firstName,
        lastName: this.state.lastName,
        email: this.state.email
      })
    } else {
      alert(response.content)
    }
  }

  render() {
    if (this.state.isLoading) {
      return (
        <View style={styles.preloader}>
          <ActivityIndicator size="large" color="#9E9E9E" />
        </View>
      )
    }
    return (
      <View style={styles.container}>
        <Image source={require('./assets/voyagerLogo.png')} />
        <TextInput
          style={styles.inputStyle}
          placeholder="First Name"
          value={this.state.name}
          onChangeText={(val) => this.updateInputVal(val, 'firstName')}
        />
        <TextInput
          style={styles.inputStyle}
          placeholder="Last Name"
          value={this.state.name}
          onChangeText={(val) => this.updateInputVal(val, 'lastName')}
        />
        <TextInput
          style={styles.inputStyle}
          placeholder="Email"
          value={this.state.email}
          onChangeText={(val) => this.updateInputVal(val, 'email')}
        />
        <TextInput
          style={styles.inputStyle}
          placeholder="Password"
          value={this.state.password}
          onChangeText={(val) => this.updateInputVal(val, 'password')}
          maxLength={15}
          secureTextEntry={true}
        />
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
          onPress={() => this.register()}
        />
        <Text
          style={styles.loginText}
          onPress={() => this.props.navigation.navigate('Login')}
        >
          Already Registered? Click here to login
        </Text>
      </View>
    )
  }
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
