import { Modal } from "../../ui/Modal"
import CloseIcon from '@mui/icons-material/Close';
import styles from './Analytics.module.scss'
import { useMemo } from "react";
import { useGetDynamicsByInterval } from "../../hooks/analytics/useGetDynamicsByInterval";
import { DynamicsByIntervalEntry } from "../../api/analytics";
import {Chart, AxisOptions} from "react-charts"


export interface AnalyticsProps {
  isOpen: boolean
  setIsOpen: (val: boolean) => void
}

export const Analytics = (props: AnalyticsProps) => {
  const {isOpen, setIsOpen} = props

  const {data} = useGetDynamicsByInterval({start: "2025-04-01", end: "2025-06-01", interval: "week"})
  

  const primaryAxis = useMemo((): AxisOptions<DynamicsByIntervalEntry> => {
    return {
      getValue: (data: DynamicsByIntervalEntry) => data.date
    }
  }, [])

  const secondaryAxes = useMemo((): AxisOptions<DynamicsByIntervalEntry>[] => {
    return [{
      getValue: (data: any) => data.count
    }]
  }, [])


  return (
    <Modal isOpen={isOpen}>
      <div className={styles.form}>
        <CloseIcon className={styles.close} onClick={() => setIsOpen(false)}/>
        <h1>Динамика транзакций</h1>
        {data && <Chart
          options={{
            data: data,
            primaryAxis,
            secondaryAxes,
            padding: {
              left: 24,
              top: 48,
              bottom: 24,
              right: 24
            },
          }}
        />}
      </div>
    </Modal>
  )
}