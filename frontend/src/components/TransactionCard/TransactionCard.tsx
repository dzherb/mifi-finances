import styles from './TransactionCard.module.scss'
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';


export interface TransactionCardProps {
  data: any
  onView: (data: any) => void
  onEdit: (data: any) => void
}

export const TransactionCard = (props: TransactionCardProps) => {
  const {data, onView, onEdit} = props

  return (
    <div className={styles.tx}>
      <p>Title {data}</p>
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