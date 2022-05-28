// components/login.js
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
// import { loginUser } from '../../controller/controller'
import { responseStatus } from '../../Config/constants'
import { alert } from './utils'
export default class Login extends Component {
  constructor(props) {
    super()
    this.state = {
      email: 'gil@g.com',
      password: 'Aa12345678!',
      isLoading: false,
      controller: props.route.params.controller
    }
  }
  updateInputVal = (val, prop) => {
    const state = this.state
    state[prop] = val
    this.setState(state)
  }
  userLogin = async () => {
    const { email, password, role } = this.state
    const response = await this.state.controller.loginUser(
      email,
      password,
      role
    )
    if (response.status === responseStatus.SUCCESS) {
      this.props.navigation.navigate('BluetoothScreen', {
        consumer: response.content
      })
    } else {
      alert('Error', response.content)
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
        <Picker
          selectedValue={this.state.role}
          onValueChange={(itemValue, itemIndex) =>
            this.setState({ role: itemValue })
          }
          style={styles.inputStyle}
        >
          <Picker.Item label="Consumer" value="Consumer" />
          <Picker.Item label="Voyager Manager" value="Voyager Manager" />
          <Picker.Item label="Care Giver" value="Care Giver" />
        </Picker>
        <Button
          color="#3740FE"
          title="Login"
          onPress={() => this.userLogin()}
        />
        <Text
          style={styles.loginText}
          onPress={() => this.props.navigation.navigate('SignUp')}
        >
          Don't have account? Click here to signup
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
