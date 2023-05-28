import { CCard, CCardBody, CCardHeader } from '@coreui/react'
import { useEffect, useState } from 'react'
import DataTable from 'react-data-table-component'
import API from 'src/utils/Api'

const Incident = () => {
  const [items, setItems] = useState([])
  const [totalRows, setTotalRows] = useState(0)
  const [limit, setLimit] = useState(10)
  const endpoint = '/incident'
  const title = 'Полученные инциденты'

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
      selector: (row) => (row.event ? row.event.name : '-'),
    },
    {
      name: 'Источник',
      selector: (row) => (row.event.source ? row.event.source.name : '-'),
    },
    {
      name: 'Дата открытия',
      selector: (row) => row.date_system_create,
    },
    {
      name: 'Дата закрытия',
      selector: (row) => row.date_close,
    },
  ]

  useEffect(() => {
    get_list()
    get_count()
  }, [limit])

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
export default Incident
