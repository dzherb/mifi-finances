import { useIsAuth } from '../../hooks/auth'
import { Button } from '../../ui/Button'
import styles from './Header.module.scss'

export const Header = () => {
  const {data: isAuth} = useIsAuth()

  return (
    <div className={styles.header}>
      <h1>Мои финансы</h1>
      <span>
        {isAuth && <Button>Выход</Button>}
      </span>
    </div>
  )
}