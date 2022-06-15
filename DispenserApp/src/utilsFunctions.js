export const createResponseObj = (status, content) => ({
  status: status,
  content: content
})

export const toDateString = (date) => date.toISOString().split('T')[0]

export const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    )
}

export const checkStrongPassword = (pwd) => {
  return (
    pwd.match(/[A-Z]/) &&
    pwd.match(/[a-z]/) &&
    pwd.match(/\d/) &&
    pwd.match(/[!_.-]/)
  )
}

export const checkTheParametersAreValid = (...args) =>
  args.every((arg) => (console.log(args), arg !== ''))
