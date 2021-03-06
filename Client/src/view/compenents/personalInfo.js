// components/login.js
import React, { useState } from 'react'
import { ResourceIds as ids } from './ResourceIds'
import { StyleSheet, Text, View, TextInput, Button, Alert } from 'react-native'
import { Picker } from '@react-native-picker/picker'
// import { createConsumerProfile } from '../../controller/controller'
import { responseStatus } from '../../Config/constants'
import { alert } from './utils'
export default function PersonalInfo({ navigation, route }) {
  const [birthDate, setBirthDate] = useState(new Date())
  const [dateModalOpen, setDateModalOpen] = useState(false)
  const [height, setHeight] = useState(100)
  const [weight, setWeight] = useState(30)
  const [gender, setGender] = useState('Male')
  const [residence, setResidence] = useState(0)
  const [controller, setConroller] = useState(route.params.controller)

  function range(start, end) {
    const output = Array(end - start + 1)
      .fill()
      .map((_, idx) => start + idx)
    return output
  }

  async function onSubmit() {
    const response = await controller.createConsumerProfile(
      residence,
      height,
      weight,
      1,
      1,
      'N/A',
      route.params
    )
    if (response.status === responseStatus.SUCCESS) {
      console.log(response.content)
      navigation.navigate('BluetoothScreen', {
        consumer: response.content
      })
    } else {
      alert('Error', response.content)
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Personal Information</Text>
      <View style={styles.option}>
        <Text>Pick your height</Text>
        <Picker
          selectedValue={height.toString()}
          onValueChange={(itemValue, itemIndex) => setHeight(itemValue)}
          style={styles.inputNumberStyle}
        >
          {range(100, 250).map((heightInRange) => (
            <Picker.Item
              label={heightInRange.toString()}
              value={heightInRange.toString()}
            />
          ))}
        </Picker>
        <Text>cm</Text>
      </View>
      <View style={styles.option}>
        <Text>Pick your weight</Text>
        <Picker
          selectedValue={weight.toString()}
          onValueChange={(itemValue, itemIndex) => setWeight(itemValue)}
          style={styles.inputNumberStyle}
        >
          {range(30, 170).map((weightInRange) => (
            <Picker.Item
              label={weightInRange.toString()}
              value={weightInRange.toString()}
            />
          ))}
        </Picker>
        <Text>kg</Text>
      </View>
      <View style={styles.option}>
        <Text>Pick your gender</Text>
        <Picker
          selectedValue={weight.toString()}
          onValueChange={(itemValue, itemIndex) => setWeight(itemValue)}
          style={styles.inputWordStyle}
        >
          <Picker.Item label={'Male'} value={'Male'} />
          <Picker.Item label={'Female'} value={'Female'} />
        </Picker>
      </View>
      <View style={styles.option}>
        <Text>Enter you zip</Text>
        <TextInput
          style={styles.inputStyle}
          value={residence}
          placeholder={'1234'}
          onChangeText={(val) => setResidence(val)}
          keyboardType="numeric"
          maxLength={6}
          testID={ids.regPersonalInfo_residence_et}
        />
      </View>
      <Button title="Submit" onPress={(e) => onSubmit()} testID={ids.regPersonalInfo_submit_btn}/>
    </View>
  )
}
const styles = StyleSheet.create({
  header: {
    fontSize: 30,
    alignContent: 'flex-start',
    marginBottom: 40
  },
  option: {
    display: 'flex',
    flexDirection: 'row-reverse',
    right: 10,
    width: '100%',
    justifyContent: 'space-between',
    marginBottom: 15,
    paddingBottom: 15,
    alignSelf: 'center',
    borderColor: '#ccc',
    borderBottomWidth: 1
  },
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    padding: 35,
    backgroundColor: '#fff'
  },
  inputWordStyle: {
    width: '50%'
  },
  inputNumberStyle: {
    width: '40%'
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
