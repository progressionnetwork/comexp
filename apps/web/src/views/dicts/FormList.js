import { CCard, CCardBody, CCardHeader } from '@coreui/react'
import { useEffect, useState } from 'react'
import DataTable from 'react-data-table-component'
import { useLocation } from 'react-router-dom'
import API from 'src/utils/Api'
import routes from '../../routes'

const FormList = () => {
  const [items, setItems] = useState([])
  const [totalRows, setTotalRows] = useState(0)
  const [limit, setLimit] = useState(10)
  const currentLocation = useLocation().pathname

  const getRouteName = (pathname, routes) => {
    const currentRoute = routes.find((route) => route.path === pathname)
    return currentRoute ? currentRoute.name : false
  }

  const getRoutePath = (pathname, routes) => {
    const currentRoute = routes.find((route) => route.path === pathname)
    return currentRoute ? currentRoute.path : false
  }
  const endpoint = getRoutePath(currentLocation, routes)
  const title = getRouteName(currentLocation, routes)

  const get_list = async (offset = 1) => {
    const response = await API.get(`${endpoint}/?offset=${(offset - 1) * limit}&limit=${limit}`)
    setItems(response.data)
  }

  const get_count = async () => {
    const response = await API.get(`${endpoint}/count/`)
    setTotalRows(response.data)
  }

  const columns = [
    {
      name: '#',
      selector: (row) => row.id,
      maxWidth: '100px',
    },
    {
      name: 'Наименование',
      selector: (row) => row.name,
    },
  ]

  useEffect(() => {
    get_list()
    get_count()
  }, [limit, currentLocation])

  return (
    <CCard>
      <CCardHeader>
        <h4>{title}</h4>
      </CCardHeader>
      <CCardBody>
        <DataTable
          // className="rounded-4"
          columns={columns}
          data={items}
          direction="auto"
          pagination
          paginationServer
          responsive
          subHeaderAlign="right"
          subHeaderWrap
          paginationTotalRows={totalRows}
          onChangePage={(offset) => {
            get_list(offset)
          }}
          onChangeRowsPerPage={(newPerPage, page) => {
            setLimit(newPerPage)
          }}
        />
      </CCardBody>
    </CCard>
  )
}
export default FormList
