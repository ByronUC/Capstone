import { useState, useRef, useEffect } from "react"
import { DayPicker } from "react-day-picker"
import { format } from "date-fns"
import { es } from "date-fns/locale"
import { Box, Input } from "@chakra-ui/react"
import { FaCalendarAlt } from "react-icons/fa"

interface DatePickerInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  size?: "lg" | "sm" | "md" | "xl" | "2xl" | "2xs" | "xs"
}

export function DatePickerInput({ value, onChange, placeholder = "Selecciona una fecha", size = "lg" }: DatePickerInputProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(value ? new Date(value) : undefined)
  const inputRef = useRef<HTMLDivElement>(null)
  const pickerRef = useRef<HTMLDivElement>(null)

  console.log("DatePickerInput rendered - isOpen:", isOpen)

  // Convertir string YYYY-MM-DD a Date
  useEffect(() => {
    if (value) {
      setSelectedDate(new Date(value))
    }
  }, [value])

  // Cerrar al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        inputRef.current &&
        !inputRef.current.contains(event.target as Node) &&
        pickerRef.current &&
        !pickerRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  const handleDaySelect = (date: Date | undefined) => {
    setSelectedDate(date)
    if (date) {
      // Convertir a formato YYYY-MM-DD
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, "0")
      const day = String(date.getDate()).padStart(2, "0")
      onChange(`${year}-${month}-${day}`)
      setIsOpen(false)
    }
  }

  const displayValue = selectedDate ? format(selectedDate, "dd 'de' MMMM 'de' yyyy", { locale: es }) : ""

  return (
    <Box position="relative" ref={inputRef}>
      <Box position="relative">
        <Input
          value={displayValue}
          onClick={() => {
            console.log("Input clicked! Opening calendar")
            setIsOpen(!isOpen)
          }}
          placeholder={placeholder}
          readOnly
          cursor="pointer"
          size={size}
          bg="white"
          borderColor="gray.300"
          _hover={{ borderColor: "blue.400" }}
          _focus={{ borderColor: "blue.500", boxShadow: "0 0 0 1px var(--chakra-colors-blue-500)" }}
          fontWeight="500"
          pr="40px"
        />
        <Box
          position="absolute"
          right="12px"
          top="50%"
          transform="translateY(-50%)"
          pointerEvents="none"
          color="blue.500"
        >
          <FaCalendarAlt />
        </Box>
      </Box>

      {isOpen && (
          <Box
            ref={pickerRef}
            position="absolute"
            top="100%"
            left={0}
            mt={2}
            zIndex={9999}
            bg="white"
            boxShadow="2xl"
            borderRadius="xl"
            border="1px solid"
            borderColor="gray.200"
            p={3}
            maxW="320px"
            css={{
              "& .rdp": {
                margin: 0,
                fontSize: "14px",
              },
              "& .rdp-root": {
                "--rdp-accent-color": "#3182ce",
                "--rdp-accent-background-color": "#ebf8ff",
              },
              "& .rdp-caption": {
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                marginBottom: "12px",
              },
              "& .rdp-caption_label": {
                display: "none",
              },
              "& .rdp-dropdowns": {
                display: "flex !important",
                gap: "8px",
                justifyContent: "center",
                alignItems: "center",
                width: "100%",
              },
              "& .rdp-dropdown_month, & .rdp-dropdown_year": {
                padding: "8px 12px",
                fontSize: "15px",
                fontWeight: 600,
                border: "2px solid #e2e8f0",
                borderRadius: "8px",
                backgroundColor: "white",
                color: "#2d3748",
                cursor: "pointer",
                transition: "all 0.2s",
              },
              "& .rdp-dropdown_month": {
                minWidth: "130px",
              },
              "& .rdp-dropdown_year": {
                minWidth: "90px",
              },
              "& .rdp-dropdown_month:hover, & .rdp-dropdown_year:hover": {
                borderColor: "#3182ce",
                backgroundColor: "#ebf8ff",
              },
              "& .rdp-dropdown_month:focus, & .rdp-dropdown_year:focus": {
                outline: "none",
                borderColor: "#3182ce",
                boxShadow: "0 0 0 3px rgba(49, 130, 206, 0.1)",
              },
              "& .rdp-day": {
                width: "32px",
                height: "32px",
                fontSize: "13px",
              },
              "& .rdp-day_button": {
                borderRadius: "6px",
                transition: "all 0.2s",
                fontWeight: 500,
                width: "100%",
                height: "100%",
              },
              "& .rdp-day_button:hover:not([disabled])": {
                backgroundColor: "#ebf8ff",
                color: "#2c5282",
              },
              "& .rdp-day_button[aria-selected='true']": {
                backgroundColor: "#3182ce !important",
                color: "white !important",
                fontWeight: 600,
              },
              "& .rdp-day_button[aria-current='date']": {
                fontWeight: 700,
                color: "#3182ce",
              },
              "& .rdp-weekday": {
                color: "#718096",
                fontWeight: 600,
                fontSize: "11px",
                textTransform: "uppercase",
              },
              "& .rdp-nav": {
                display: "none",
              },
            }}
          >
            <DayPicker
              mode="single"
              selected={selectedDate}
              onSelect={handleDaySelect}
              locale={es}
              showOutsideDays
              captionLayout="dropdown"
              startMonth={new Date(1920, 0)}
              endMonth={new Date()}
            />
          </Box>
      )}
    </Box>
  )
}
