import { CCard, CCardBody, CCardHeader } from '@coreui/react'
import { useEffect, useState } from 'react'
import DataTable from 'react-data-table-component'

const APIService = () => {
  const [items, setItems] = useState([])
  const [totalRows, setTotalRows] = useState(0)
  const [limit, setLimit] = useState(10)

  const title = 'Источники данных: Apache Kafka'

  const get_list = async (offset = 1) => {
    setItems([
      {
        id: 1,
        name: 'https://kafka.comexp.intellectg.ru:9092',
      },
    ])
  }

  const get_count = async () => {
    setTotalRows(1)
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
      name: 'Топики',
      selector: (row) => 'MOS_GAS, CAFAP, GORMOST, KGH, EVAGD',
    },
    {
      name: 'Получено за последние сутки',
      selector: (row) => '0',
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
