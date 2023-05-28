import { CButton, CCard, CCardBody, CCardHeader, CCol, CForm, CFormSelect } from '@coreui/react'
import ru from 'date-fns/locale/ru'
import { useState } from 'react'
import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import { useDispatch, useSelector } from 'react-redux'
import { setCategory, setEndDate, setSource, setStartDate } from 'src/redux/dashboardFilter'
const DashboardFilter = () => {
  const [listCategory, setListCategery] = useState([])
  const [listSource, setListSource] = useState([])

  const dispatch = useDispatch()
  const category = useSelector((state) => state.dashboard.filter.category)
  const source = useSelector((state) => state.dashboard.filter.source)
  const startDate = useSelector((state) => state.dashboard.filter.startDate)
  const endDate = useSelector((state) => state.dashboard.filter.endDate)
  console.log(category, source, startDate, endDate)
  return (
    <CCard className="mb-5">
      <CCardHeader>
        <h4 id="traffic" className="card-title mb-0">
          Фильтр
        </h4>
      </CCardHeader>
      <CCardBody className="col justify-content-center">
        <CForm className="m-1 row row-cols-lg-auto g-3 align-items-end  justify-content-between">
          <CCol xs={12}>
            <h6>Категория</h6>
            <CFormSelect
              options={[
                'Выберите категорию',
                { label: 'One', value: '1' },
                { label: 'Two', value: '2' },
                { label: 'Three', value: '3', disabled: true },
              ]}
              defaultValue={category}
              onChange={(event) => dispatch(setCategory(event.target.value))}
            />
          </CCol>
          <CCol xs={12}>
            <h6>Источник</h6>
            <CFormSelect
              options={[
                'Выберите источник',
                { label: 'One', value: '1' },
                { label: 'Two', value: '2' },
                { label: 'Three', value: '3', disabled: true },
              ]}
              defaultValue={source}
              onChange={(event) => dispatch(setSource(event.target.value))}
            />
          </CCol>
          <CCol xs={12}>
            <h6>Начало периода</h6>
            <DatePicker
              className="form-control"
              locale={ru}
              selected={startDate}
              onChange={(date) => dispatch(setStartDate(date.getTime()))}
              dateFormat="dd.MM.yyyy"
            />
          </CCol>
          <CCol xs={12}>
            <h6>Окончание периода</h6>
            <DatePicker
              className="form-control"
              locale={ru}
              selected={endDate}
              onChange={(date) => dispatch(setEndDate(date.getTime()))}
              dateFormat="dd.MM.yyyy"
            />
          </CCol>
          <CButton>Применить</CButton>
        </CForm>
      </CCardBody>
    </CCard>
  )
}

export default DashboardFilter
