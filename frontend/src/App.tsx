import styles from "./App.module.scss"
import { AuthModal } from "./components/AuthModal/AuthModal"
import { Header } from './components/Header'
import { useIsAuth } from "./hooks/auth"
import { MainPage } from "./pages/MainPage"

function App() {
  const {data: isAuth} = useIsAuth()

  return (
    <>
      <div className={styles.app}>
        <Header/>
        <div className={styles.pageWrap}>
          <MainPage/>
        </div>
      </div>
      {<AuthModal isOpen={!isAuth}/>}
    </>
  )
}

export default App
