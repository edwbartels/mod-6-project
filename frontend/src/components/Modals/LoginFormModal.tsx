import { useState } from "react"
import { useModal } from "../../context/Modal"
import { Errors } from "../Errors/Errors"

export const LoginFormModal = () => {
  const [loginForm, setLoginForm] = useState({
    credential: "",
    password: "",
  })
  const [errors, setErrors] = useState({})
  const { closeModal } = useModal()

  // Disable submit button if credential length < 4 or password length < 6
  const isDisabledSubmit =
    loginForm.credential.length < 4 || loginForm.password.length < 6

  const handleChangeLoginForm =
    (loginFormField: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
      setLoginForm({
        ...loginForm,
        [loginFormField]: e.target.value,
      })
    }

  const handleSubmitLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setErrors({})
    // Send login request to back end
    // Set errors if any come back
    closeModal()
  }

  const handleLogInDemo = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    setErrors({})
    closeModal()
  }

  return (
    <div className="login-form" data-testid="login-modal">
      <Errors errors={errors} />
      <form onSubmit={handleSubmitLogin}>
        <div>
          <label className="login-form-item">
            <div>Username/email</div>
            <input
              onChange={handleChangeLoginForm("credential")}
              defaultValue={loginForm.credential}
              placeholder="Username/email"
              name="credential"
              type="text"
              required
            />
          </label>
        </div>
        <div>
          <label className="login-form-item">
            <div>Password</div>
            <input
              onChange={handleChangeLoginForm("password")}
              placeholder="Password"
              defaultValue={loginForm.password}
              name="password"
              type="password"
              required
            />
          </label>
        </div>
        <button
          disabled={isDisabledSubmit}
          data-testid="login-button" // Identifier
        >
          Log In
        </button>
      </form>
      <button onClick={handleLogInDemo} data-testid="demo-user-login">
        Log in Demo User
      </button>
    </div>
  )
}