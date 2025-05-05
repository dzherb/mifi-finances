import { useQueryClient } from '@tanstack/react-query'
import { ACCESS, REFRESH, setCookie } from '../../api/axios'
import { useIsAuth } from '../../hooks/auth'
import { Button } from '../../ui/Button'
import styles from './Header.module.scss'

export const Header = () => {
  const {data: isAuth} = useIsAuth()
  const queryClient = useQueryClient()

  return (
    <div className={styles.header}>
      <h1>Мои финансы</h1>
      <span>
        {isAuth && <Button onClick={() => {
          setCookie(REFRESH, '')
          localStorage.setItem(ACCESS, '')
          queryClient.invalidateQueries({queryKey: ['auth']})
          queryClient.invalidateQueries({queryKey: ['user']})
        }}>Выход</Button>}
      </span>
    </div>
  )
}