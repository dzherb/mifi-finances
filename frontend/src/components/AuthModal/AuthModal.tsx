import { useState } from "react"
import { Modal } from "../../ui/Modal"
import { TextInput } from "../../ui/TextInput"
import { Button } from "../../ui/Button"
import { useCreateAccaunt, useLogin } from "../../hooks/auth"
import styles from './AuthModal.module.scss'
import clsx from "clsx"

export interface AuthFormProps {
  isOpen: boolean
}

export const AuthModal = (props: AuthFormProps) => {
  const {isOpen} = props

  const login = useLogin()
  const create = useCreateAccaunt()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [mode, setMode] = useState("login")
  const changeMode = () => {
    if (mode === "login") { setMode("create")}
    else {setMode("login")}
  }

  return (
    <Modal isOpen={isOpen}>
      <div className={styles.modal}>
        <h1>
          {mode === "login" ? "Авторизация" : "Создание аккаунта"}
        </h1>

        <TextInput 
          label="E-mail" 
          value={email} 
          setValue={setEmail}
          placeholder="Введите e-mail"
          autoComplete="email"
          name="email"
          type="email"
        />
        <TextInput 
          label="Пароль" 
          value={password} 
          setValue={setPassword} 
          placeholder="Введите пароль"
          autoComplete="current-password"
          name="password"
          type="password"
        />

        <p 
          className={clsx("small", styles.mode)}
          onClick={changeMode}
        >
            {mode === "login" ? "Регистрация" : "Войти в аккаунт"}
        </p>

        <Button 
          onClick={async (e) => {
            e.preventDefault()
            
            if (mode === "login") {
              login.mutate({email, password}, {onError: () => {alert("Введены некорректные данные")}})
            } else {
              create.mutate({email, password}, {onError: () => {alert("Аккаунт с такой почтой уже существует")}})
              setMode("login")
            }

            setEmail('')
            setPassword('')
          }}
        >
          <p>{mode === "login" ? "Войти" : "Создать"}</p>
        </Button>

      </div>
    </Modal>
  )
}