import styles from "./App.module.scss"
import { AuthModal } from "./components/AuthModal/AuthModal"
import { Header } from './components/Header'
import { useIsAuth } from "./hooks/auth"
import { useGetUser } from "./hooks/user"
import { AdminPage } from "./pages/AdminPage"
import { MainPage } from "./pages/MainPage"

function App() {
  const {data: isAuth} = useIsAuth()
  const {data: user} = useGetUser()

  if (!isAuth) {
    return <AuthModal isOpen={true}/>
  }

  return (
    <>
      <div className={styles.app}>
        <Header/>
        <div className={styles.pageWrap}>
          {user?.is_admin ? <AdminPage/> : <MainPage/>}
        </div>
      </div>
    </>
  )
}

export default App
