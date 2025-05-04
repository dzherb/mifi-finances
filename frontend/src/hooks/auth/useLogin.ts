import { useMutation, useQueryClient } from "@tanstack/react-query"
import { login } from "../../api/user.api"

interface ILoginParams {
  email: string
  password: string
}

export function useLogin() {
  const queryClient = useQueryClient()

  const mutation = useMutation(
    {
      mutationFn: async ({ email, password }: ILoginParams) => {
        const res = await login(email, password)
        await queryClient.invalidateQueries({ queryKey: ['isAuth'] })

        return res
      },

    }
  )

  return mutation
}