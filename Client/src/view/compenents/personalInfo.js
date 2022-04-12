// components/login.js
import React, { useState } from 'react'
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  Button,
  Alert,
  ActivityIndicator,
  Header
} from 'react-native'
import { Picker } from '@react-native-picker/picker'
import DatePicker from 'react-native-date-picker'
import RNNumberPickerLibrary from 'react-native-number-picker-library'

export default function PersonalInfo({ navigation }) {
  const [birthDate, setBirthDate] = useState(new Date())
  const [dateModalOpen, setDateModalOpen] = useState(false)
  const [height, setHeight] = useState(100)
  const [weight, setWeight] = useState(30)
  const [gender, setGender] = useState()

  function range(start, end) {
    const output = Array(end - start + 1)
      .fill()
      .map((_, idx) => start + idx)
    console.log(output)
    return output
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Personal Information</Text>
      <View style={styles.option}>
        <Button
          title="Pick Year Of Birth"
          onPress={() => setDateModalOpen(true)}
        />
        <Text>{birthDate.toDateString()}</Text>
      </View>
      <View style={styles.option}>
        <Text>Pick your height</Text>
        <Picker
          selectedValue={height.toString()}
          onValueChange={(itemValue, itemIndex) => setHeight(itemValue)}
          style={styles.inputStyle}
        >
          {range(height, height + 100).map((heightInRange) => (
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
          style={styles.inputStyle}
        >
          {range(weight, weight + 170).map((weightInRange) => (
            <Picker.Item
              label={weightInRange.toString()}
              value={weightInRange.toString()}
            />
          ))}
        </Picker>
        <Text>kg</Text>
      </View>
      <DatePicker
        modal
        open={dateModalOpen}
        date={birthDate}
        onConfirm={(date) => {
          setBirthDate(date)
        }}
        onCancel={() => {
          setDateModalOpen(setDateModalOpen(false))
        }}
      />
    </View>
  )
}
const styles = StyleSheet.create({
  header: {
    fontSize: 30,
    alignContent: 'flex-start',
    marginBottom: 40,
    borderBottomWidth: 1
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
  inputStyle: {
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
