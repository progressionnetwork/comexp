import { CButton, CCard, CCardBody, CCardHeader } from '@coreui/react'
import { useEffect, useState } from 'react'
import DataTable from 'react-data-table-component'

const APIService = () => {
  const [items, setItems] = useState([])
  const [totalRows, setTotalRows] = useState(0)
  const [limit, setLimit] = useState(10)

  const title = 'Источники данных: API сервисы'

  const get_list = async (offset = 1) => {
    setItems([
      {
        id: 1,
        name: 'https://building-api.comexp.intellectg.ru',
      },
      {
        id: 2,
        name: 'https://incident-api.comexp.intellectg.ru',
      },
      {
        id: 3,
        name: 'https://work-api.comexp.intellectg.ru',
      },
    ])
  }

  const get_count = async () => {
    setTotalRows(3)
  }

  const columns = [
    {
      name: '#',
      selector: (row) => row.id,
      maxWidth: '100px',
    },
    {
      name: 'Сервер',
      selector: (row) => row.name,
    },
    {
      name: 'Действия',
      button: true,
      cell: (row) => (
        <CButton id={row.id} size="sm" color="success" variant="outline" className="m-1">
          Запрос
        </CButton>
      ),
      minWidth: '300px',
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
export default APIService
