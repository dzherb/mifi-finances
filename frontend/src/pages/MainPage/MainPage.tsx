import { useState } from 'react'
import { Button } from '../../ui/Button'
import styles from './MainPage.module.scss'
import { TransactionFormModal, TTransactionFormMode } from '../../components/TransactionFormModal'
import { TransactionCard } from '../../components/TransactionCard'
import TuneIcon from '@mui/icons-material/Tune';
import {Pagination} from '@mui/material';
import { FiltersModal } from '../../components/FiltersModal'
import { useGetTransactions } from '../../hooks/transaction/useGetTransactions'
import { Transaction } from '../../api/transaction.api'
import EqualizerIcon from '@mui/icons-material/Equalizer';
import { Analytics } from '../../components/Analytics'


const LIMIT = 10;

export const MainPage = () => {

  const [transactionFormMode, setTransactionFormMode] = useState<TTransactionFormMode>()
  const [defaultData, setDefaultData] = useState<Transaction>()

  const [filtersData, setFiltersData] = useState()
  const [filtersOpen, setFiltersOpen] = useState(false)
  const [analyticsOpen, setAnalyticsOpen] = useState(false)

  const [page, setPage] = useState(1)
  const {data: transactions} = useGetTransactions({limit: LIMIT, offset: (page-1) * LIMIT})

  return (
    <div className={styles.mainPage}>

      <div className={styles.txWrap}>
        {transactions?.map(tx => (
          <TransactionCard 
            key={tx.id} 
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

      <Button className={styles.analytics} onClick={() => {setAnalyticsOpen(true)}}>
        <EqualizerIcon/>
      </Button>

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
      {analyticsOpen && <Analytics isOpen={analyticsOpen} setIsOpen={setAnalyticsOpen}/>}
    </div>


  )
}