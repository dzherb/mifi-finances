import { useQuery } from "@tanstack/react-query"
import { checkAuth } from "../../api/user.api"


export const useIsAuth = () => {
  const response = useQuery({
    queryKey: ['isAuth'],
    queryFn: async () => {
      let isAuth = await checkAuth()
      return isAuth
    }
  })

  return response
}