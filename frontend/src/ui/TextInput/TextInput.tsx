import MuiTextField from '@mui/material/TextField';
import styles from './TextInput.module.scss'
import clsx from 'clsx';
import { ComponentProps } from 'react';

export interface ITextInput extends ComponentProps<"input"> {
  label: string
  type?: string
  pattern?: string
  maxLength?: number;
  value?: string
  setValue: (v: string) => void
  helperText?: string
  className?: string
  style?: Object
  onEnter?: () => void
}

export const TextInput = (props: ITextInput) => {
  const {label, type, pattern, maxLength, value, setValue, helperText, className, style, onEnter, disabled} = props

  return (
    <MuiTextField
      label={label}
      type={type}
      value={value}
      onChange={e => {setValue(e.target.value)}}
      className={clsx(styles.root, className)}
      style={style}
      onKeyDown={e => {
        if (e.code === 'Enter') {
          onEnter?.()
        }
      }}
      inputProps={{pattern, maxLength}}
      helperText={helperText}
      disabled={disabled}
    />
  )
}