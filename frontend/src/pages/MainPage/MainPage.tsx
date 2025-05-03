import { useState } from 'react'
import { Button } from '../../ui/Button'
import styles from './MainPage.module.scss'
import { TransactionFormModal, TTransactionFormMode } from '../../components/TransactionFormModal'
import { TransactionCard } from '../../components/TransactionCard'
import TuneIcon from '@mui/icons-material/Tune';
import {Pagination} from '@mui/material';
import { FiltersModal } from '../../components/FiltersModal'

export const MainPage = () => {

  const [transactionFormMode, setTransactionFormMode] = useState<TTransactionFormMode>()
  const [defaultData, setDefaultData] = useState()

  const [filtersData, setFiltersData] = useState()
  const [transactions, setTransaction] = useState([1,2,3,4,5,6,7,8,9,10, 11, 12, 13, 14, 15, 16, 17])

  const [filtersOpen, setFiltersOpen] = useState(false)
  const [page, setPage] = useState(1)

  return (
    <div className={styles.mainPage}>

      <div className={styles.txWrap}>
        {transactions.map(tx => (
          <TransactionCard 
            key={tx} 
            data={tx} 
            onView={(data) => {
              setDefaultData(data)
              setTransactionFormMode("view")
            }}
            onEdit={(data) => {
              setDefaultData(data)
              setTransactionFormMode("edit")
            }}
          />
        ))}
      </div>

      <div className={styles.pagination}>
        <Pagination count={10} page={page} onChange={(_, page) => {setPage(page)}}/>
      </div>

      <div className={styles.menu}>
        <Button onClick={() => {
          setFiltersOpen(true)
        }}>
          <TuneIcon/>
        </Button>
        <Button
          onClick={() => {
            setDefaultData(undefined)
            setTransactionFormMode("add")
          }}
        >
          Добавить транзакцию
        </Button>
      </div>

      {filtersOpen && <FiltersModal isOpen={filtersOpen} setIsOpen={setFiltersOpen} data={filtersData} setData={setFiltersData}/>}
      {!!transactionFormMode && <TransactionFormModal mode={transactionFormMode} setMode={setTransactionFormMode} defaultData={defaultData}/>}
    </div>


  )
}