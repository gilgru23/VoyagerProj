const prod = true
export const baseURL = prod ? 'http://3.134.98.86' : 'http://127.0.0.1:8000'
export const responseStatus = {
  SUCCESS: 'success',
  FAILURE: 'failure'
}

export const msgsFromDispenserTypes = {
  POD_RUNNING_LOW: 'pod running low',
  DOSING: 'dosing'
}

export const timeIntervalForFeedbackReminder = 1
