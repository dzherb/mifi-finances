import { useState } from 'react'
import { Button } from '../../ui/Button'
import { TextInput } from '../../ui/TextInput'
import styles from './AdminPage.module.scss'
import { useGetBanks } from '../../hooks/bank/useGetBanks'
import { useGetTransactionsCategories } from '../../hooks/transaction/useGetCategories'
import { useAddBank } from '../../hooks/bank/useAddBank'
import { useAddCategory } from '../../hooks/transaction/useAddCategory'
import CloseIcon from '@mui/icons-material/Close';
import { useDeleteBank } from '../../hooks/bank/useDeleteBank'
import { useDeleteCategory } from '../../hooks/transaction/useDeleteCategory'

export const AdminPage = () => {

  const [bank, setBank] = useState('')
  const [category, setCategory] = useState('')

  const {data: banks} = useGetBanks()
  const {data: categories} = useGetTransactionsCategories()

  const addBank = useAddBank()
  const deleteBank = useDeleteBank()

  const addCategory = useAddCategory()
  const deleteCategory = useDeleteCategory()


  return (
    <div className={styles.admPage}>
      <div className={styles.addWrap}>
        <div className={styles.addMenu}>
          <TextInput value={bank} setValue={setBank} label='Банк'/>
          <Button onClick={() => {
            addBank.mutate(bank)
            setBank('')
          }}>Добавить</Button>
        </div>
        <div className={styles.tagsWrap}>
          {banks?.map(bank => (
            <div className={styles.tag}>
              <p>{bank.label}</p>
              <CloseIcon className={styles.close} onClick={() => {deleteBank.mutate(bank.value.toString(), {onError: () => {alert("Невозможно удалить банк, для которого созданы транзакции")}})}}/>
            </div>
          ))}
        </div>
      </div>
      <div className={styles.addWrap}>
        <div className={styles.addMenu}>
          <TextInput value={category} setValue={setCategory} label='Категория'/>
          <Button onClick={() => {
            addCategory.mutate(category)
            setCategory('')
          }}>Добавить</Button>
        </div>
        <div className={styles.tagsWrap}>
          {categories?.map(cat => (
            <div className={styles.tag}>
              <p>{cat.label}</p>
              <CloseIcon className={styles.close} onClick={() => {deleteCategory.mutate(cat.value.toString(), {onError: () => {alert("Невозможно удалить категорию, для которой созданы транзакции")}})}}/>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}