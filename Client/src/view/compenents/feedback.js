// components/login.js
import React, { useState, useEffect } from 'react'
import { StyleSheet, Text, View, TextInput, Alert } from 'react-native'
import { Picker } from '@react-native-picker/picker'
import DateTimePicker from '@react-native-community/datetimepicker'
import PushNotification from 'react-native-push-notification'
import { Rating, AirbnbRating } from 'react-native-ratings'
import { Button, TextField } from 'react-native-ui-lib'

export default function Feeback({ navigation, route }) {
  const [dateModalOpen, setDateModalOpen] = useState(false)
  const [timeModalOpen, setTimeModalOpen] = useState(false)
  const [alarmDate, setAlarmDate] = useState(
    new Date(new Date().setSeconds(0, 0))
  )
  const [starCount, setStarCount] = useState(1)
  const [feedback, setFeedback] = useState('')
  const INPUT_SPACING = 10

  useEffect(() => {
    PushNotification.getScheduledLocalNotifications((notifications) =>
      notifications.forEach((notifcation) => console.log(notifcation))
    )
  }, [])
  function onSubmit() {}

  const onChangeDatePicker = (event, selectedDate) => {
    console.log(alarmDate)
    setAlarmDate(selectedDate)
    setDateModalOpen(false)
  }

  const onChangeTimePicker = (event, selectedDate) => {
    setAlarmDate(selectedDate)
    setTimeModalOpen(false)
  }
  const ratingCompleted = (rating) => {
    setStarCount(rating)
  }
  const { podSerialNum, podType, time } = route.params.dosing
  return (
    <View style={styles.container}>
      <Text
        style={styles.header}
      >{`Feedback for dosing with pod: ${podSerialNum} of type ${podType} on time ${time}`}</Text>
      <View style={styles.option}>
        <AirbnbRating
          count={5}
          reviews={['Terrible', 'Bad', 'OK', 'Good', 'Amazing']}
          defaultRating={starCount}
          size={20}
          onFinishRating={ratingCompleted}
        />
      </View>
      <TextField
        text70
        containerStyle={{ marginBottom: INPUT_SPACING }}
        placeholder="Tell us about your dosing experience"
        multiline
        maxLength={150}
        onChangeText={(text) => setFeedback(text)}
        autoCapitalize="words"
      />
      <Button
        backgroundColor="green"
        label="Submit"
        borderRadius={7}
        onPress={() => console.log('submitted')}
      />
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
    width: '100%',
    marginBottom: 30,
    paddingBottom: 15,
    borderColor: '#ccc',
    borderBottomWidth: 1
  },
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    padding: 20,
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
