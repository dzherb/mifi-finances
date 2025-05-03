import styles from './TransactionCard.module.scss'
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import { Transaction } from '../../api/transaction.api';


export interface TransactionCardProps {
  data: Transaction
  onView: (data: Transaction) => void
  onEdit: (data: Transaction) => void
}

export const TransactionCard = (props: TransactionCardProps) => {
  const {data, onView, onEdit} = props

  const date = data.occurred_at.split('T')[0] + ' ' + data.occurred_at.split('T')[1].split('.')[0]

  return (
    <div className={styles.tx}>
      <p style={{fontSize: '.8em'}}>{date}</p>
      <p>{parseInt(data.amount)}₽</p>
      {data.comment && <p>({data.comment})</p>}
      <EditIcon 
        className={styles.edit}
        onClick={() => {onEdit(data)}}
      />
      <VisibilityIcon 
        className={styles.view}
        onClick={() => {onView(data)}}
      />
      <DeleteIcon className={styles.delete}/>
    </div>
  )
}