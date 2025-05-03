import { useMutation } from "@tanstack/react-query"
import { createAccaunt } from "../../api/user.api"


interface ICreateAccauntParams {
  email: string
  password: string
}

export function useCreateAccaunt() {
  const mutation = useMutation(
    {
      mutationFn: async ({ email, password }: ICreateAccauntParams) => {
        return await createAccaunt(email, password)
      }
    }
  )

  return mutation
}