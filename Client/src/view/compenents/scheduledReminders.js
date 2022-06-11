// components/login.js
import React, { useState, useEffect } from 'react'
import { StyleSheet, Text, View, TextInput, Alert } from 'react-native'
import PushNotification from 'react-native-push-notification'
import { alert } from './utils'
import { Switch, Button } from 'react-native-ui-lib'
import AsyncStorage from '@react-native-async-storage/async-storage'

export default function ScheduledReminders({ navigation, route }) {
  const [alarmDate, setAlarmDate] = useState(
    new Date(new Date().setSeconds(0, 0))
  )
  const [scheduledReminders, setScheduledReminders] = useState([])

  useEffect(() => {
    const addActiveReminders = () => {
      PushNotification.getScheduledLocalNotifications(async (notifications) => {
        const offlineReminders = await addOfflineReminders()
        const activeReminders = notifications.map((notification) => ({
          notification: notification,
          enabled: true
        }))
        console.log('active reminders: ', activeReminders)
        setScheduledReminders([...activeReminders, ...offlineReminders])
      })
    }
    const addOfflineReminders = async () => {
      const keys = await AsyncStorage.getAllKeys()
      const result = await AsyncStorage.multiGet(keys)
      console.log('offline unparsed rminders: ', result)
      const offlineReminders = result.map((req) => ({
        notification: JSON.parse(req[1]),
        enabled: false
      }))
      console.log('offline reminders: ', offlineReminders)
      return offlineReminders
    }
    // addOfflineReminders()
    addActiveReminders()
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

  const changeReminderStatus = async (reminder) => {
    if (reminder.enabled) {
      PushNotification.cancelLocalNotification(reminder.notification.id)
      const parsedNotification = JSON.stringify(reminder.notification)
      console.log('stringify notification', parsedNotification)
      await AsyncStorage.setItem(
        `notification_${reminder.notification.id}`,
        parsedNotification
      )
    } else {
      PushNotification.localNotificationSchedule({
        channelId: route.params.consumer.email,
        date: new Date(reminder.notification.date), // in 60 secs
        title: reminder.notification.title,
        message: reminder.notification.message // (required)
      })
      await AsyncStorage.removeItem(`notification_${reminder.notification.id}`)
    }
    setScheduledReminders(
      scheduledReminders.map((scheduledReminder) =>
        reminder.notification.id === scheduledReminder.notification.id
          ? {
              notification: scheduledReminder.notification,
              enabled: !scheduledReminder.enabled
            }
          : scheduledReminder
      )
    )
  }

  const deleteReminder = async (reminder) => {
    if (reminder.enabled) {
      PushNotification.cancelLocalNotification(reminder.notification.id)
    } else {
      await AsyncStorage.removeItem(`notification_${reminder.notification.id}`)
    }
    const filteredScheduledReminders = scheduledReminders.filter(
      (scheduledReminder) =>
        scheduledReminder.notification.id !== reminder.notification.id
    )
    console.log('filtered reminders: ', filteredScheduledReminders)
    setScheduledReminders(filteredScheduledReminders)
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Current Reminders</Text>
      {
        (console.log('The reminders are', scheduledReminders),
        scheduledReminders.map((scheduledReminder) => (
          <>
            <View style={styles.reminder}>
              <Text>{`Date of dosing: ${new Date(
                scheduledReminder.notification.date
              ).toDateString()}\n Time of dosing: ${new Date(
                scheduledReminder.notification.date
              ).toTimeString()}\n Title: ${
                scheduledReminder.notification.title
              }`}</Text>
              <Switch
                value={scheduledReminder.enabled}
                onValueChange={async () =>
                  await changeReminderStatus(scheduledReminder)
                }
              />
            </View>
            <View style={styles.option}>
              <Button
                style={styles.deletButton}
                backgroundColor="red"
                label="Delete reminder"
                onPress={async () => await deleteReminder(scheduledReminder)}
                center
                size="small"
              />
            </View>
          </>
        )))
      }
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
    flexDirection: 'row',
    width: '100%',
    justifyContent: 'space-between',
    marginBottom: 15,
    paddingBottom: 15,
    alignSelf: 'center',
    borderColor: '#ccc',
    borderBottomWidth: 1
  },
  reminder: {
    display: 'flex',
    flexDirection: 'row-reverse',
    width: '100%',
    justifyContent: 'space-between',
    alignSelf: 'center'
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
