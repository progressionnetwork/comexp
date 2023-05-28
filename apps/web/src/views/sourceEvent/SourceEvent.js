import { CCard, CCardBody, CCardHeader, CListGroup, CListGroupItem } from '@coreui/react'
import { useEffect, useState } from 'react'
import DataTable from 'react-data-table-component'
import API from 'src/utils/Api'

const ExpandetComponent = (data) => {
  return (
    <CListGroup>
      {data.data.events.map((elem) => (
        <CListGroupItem component="button" key={elem.id}>
          {elem.name}
        </CListGroupItem>
      ))}
    </CListGroup>
  )
}

const SourceEvent = () => {
  const [items, setItems] = useState([])
  const [totalRows, setTotalRows] = useState(0)
  const [limit, setLimit] = useState(10)

  const endpoint = '/sourcesystem'
  const title = 'Источники событий'

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
          expandableRows={true}
          expandOnRowClicked={false}
          expandOnRowDoubleClicked={false}
          expandableRowsHideExpander={false}
          expandableRowsComponent={ExpandetComponent}
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
export default SourceEvent
