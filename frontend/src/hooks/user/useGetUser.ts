import { useQuery } from "@tanstack/react-query"
import { getUser } from "../../api/user.api"


export const useGetUser = () => {
  const response = useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      let user = await getUser()
      return user
    }
  })

  return response
}