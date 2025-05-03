import { createPortal } from "react-dom"
import { ComponentProps, useMemo } from "react"
import styles from './Modal.module.scss'

export interface ModalProps extends ComponentProps<"div"> {
  isOpen?: boolean
}

export const Modal = (props: ModalProps) => {
  const {isOpen, children} = props


  return (
    createPortal(
      <>
        {isOpen ? <div className={styles.modal}>
          {children}
        </div> : <></>}
      </>
     ,document.body)
  )
}