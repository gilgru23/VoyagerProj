// components/login.js
import React, { useState, useEffect } from 'react'
import { StyleSheet, Text, View, TextInput, Button, Alert } from 'react-native'
import { Picker } from '@react-native-picker/picker'
import DateTimePicker from '@react-native-community/datetimepicker'
import PushNotification from 'react-native-push-notification'
import { alert } from './utils'
import { Switch } from 'react-native-ui-lib'

export default function Schedule({ navigation, route }) {
  const [dateModalOpen, setDateModalOpen] = useState(false)
  const [timeModalOpen, setTimeModalOpen] = useState(false)
  const [alarmDate, setAlarmDate] = useState(
    new Date(new Date().setSeconds(0, 0))
  )
  const [scheduledReminders, setScheduledReminders] = useState([])

  useEffect(() => {
    PushNotification.getScheduledLocalNotifications((notifications) =>
      setScheduledReminders(
        notifications.map((notification) => ({
          notification: notification,
          enabled: true
        }))
      )
    )
  }, [])
  function onSubmit() {
    console.log(route.params.consumer, '*********')
    try {
      PushNotification.localNotificationSchedule({
        channelId: route.params.consumer.email || 'gilgu@gmail.com',
        date: alarmDate, // in 60 secs
        title: 'Time to dose',
        message: 'This is a reminder for dosing' // (required)
      })
      alert('Success', `Reminder has been set to ${alarmDate.toLocaleString()}`)
    } catch (e) {
      alert('Error', `Reminder creation failed`)
    }
  }

  const onChangeDatePicker = (event, selectedDate) => {
    console.log(alarmDate)
    setAlarmDate(selectedDate)
    setDateModalOpen(false)
  }

  const onChangeTimePicker = (event, selectedDate) => {
    setAlarmDate(selectedDate)
    setTimeModalOpen(false)
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Set Dosing Reminder</Text>
      {scheduledReminders.map((scheduledReminder) => (
        <View style={styles.option}>
          <Text>{`Date of dosing: ${new Date(
            scheduledReminder.notification.date
          ).toDateString()} on time: ${new Date(
            scheduledReminder.notification.date
          ).toTimeString()}`}</Text>
          <Switch
            value={true}
            onValueChange={() => console.log('value changed')}
          />
        </View>
      ))}
      <View style={styles.option}>
        <Button
          onPress={() => setDateModalOpen(true)}
          title={'Change dosing date'}
        />
        {dateModalOpen && (
          <DateTimePicker
            value={alarmDate}
            mode={'date'}
            onChange={(event, selectedDate) =>
              onChangeDatePicker(event, selectedDate)
            }
          />
        )}
      </View>
      <View style={styles.option}>
        <Button
          onPress={() => setTimeModalOpen(true)}
          title={'Change dosing time'}
        />
        {timeModalOpen && (
          <DateTimePicker
            value={alarmDate}
            display="clock"
            mode="time"
            onChange={(event, selectedTime) =>
              onChangeTimePicker(event, selectedTime)
            }
          />
        )}
      </View>
      <View style={styles.option}>
        <Text>The date and time for dosing:</Text>
        <Text>{alarmDate.toLocaleString()}</Text>
      </View>
      <Button title="Submit" onPress={(e) => onSubmit()} />
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
