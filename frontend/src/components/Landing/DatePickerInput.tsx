import { useState, useRef, useEffect } from "react"
import { DayPicker } from "react-day-picker"
import { format } from "date-fns"
import { es } from "date-fns/locale"
import { Box, Input, Portal } from "@chakra-ui/react"
import { FaCalendarAlt } from "react-icons/fa"
import "react-day-picker/style.css"

interface DatePickerInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  size?: string
}

export function DatePickerInput({ value, onChange, placeholder = "Selecciona una fecha", size = "lg" }: DatePickerInputProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(value ? new Date(value) : undefined)
  const inputRef = useRef<HTMLDivElement>(null)
  const pickerRef = useRef<HTMLDivElement>(null)

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
          onClick={() => setIsOpen(!isOpen)}
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
        <Portal>
          <Box
            ref={pickerRef}
            position="fixed"
            zIndex={9999}
            bg="white"
            boxShadow="2xl"
            borderRadius="xl"
            border="1px solid"
            borderColor="gray.200"
            p={4}
            style={{
              top: inputRef.current ? inputRef.current.getBoundingClientRect().bottom + window.scrollY + 8 : 0,
              left: inputRef.current ? inputRef.current.getBoundingClientRect().left + window.scrollX : 0,
            }}
            css={{
              ".rdp": {
                margin: 0,
                "--rdp-accent-color": "#3182ce",
                "--rdp-background-color": "#ebf8ff",
                "--rdp-accent-color-dark": "#2c5282",
                "--rdp-background-color-dark": "#bee3f8",
                "--rdp-outline": "2px solid var(--rdp-accent-color)",
                "--rdp-outline-selected": "2px solid var(--rdp-accent-color)",
              },
              ".rdp-month": {
                fontSize: "16px",
              },
              ".rdp-months": {
                justifyContent: "center",
              },
              ".rdp-month_caption": {
                fontSize: "18px",
                fontWeight: 600,
                color: "#2d3748",
                marginBottom: "12px",
                textTransform: "capitalize",
              },
              ".rdp-nav": {
                top: "12px",
              },
              ".rdp-button": {
                borderRadius: "8px",
                transition: "all 0.2s",
                fontWeight: 500,
              },
              ".rdp-day": {
                width: "42px",
                height: "42px",
                fontSize: "15px",
              },
              ".rdp-day_button:hover:not(.rdp-day_selected):not(.rdp-day_disabled)": {
                backgroundColor: "#ebf8ff",
                color: "#2c5282",
                transform: "scale(1.05)",
              },
              ".rdp-day_selected": {
                backgroundColor: "#3182ce !important",
                color: "white !important",
                fontWeight: 600,
              },
              ".rdp-day_today": {
                fontWeight: 700,
                color: "#3182ce",
              },
              ".rdp-weekday": {
                color: "#718096",
                fontWeight: 600,
                fontSize: "13px",
                textTransform: "uppercase",
                padding: "8px 0",
              },
              ".rdp-nav_button": {
                width: "36px",
                height: "36px",
                borderRadius: "8px",
                transition: "all 0.2s",
              },
              ".rdp-nav_button:hover": {
                backgroundColor: "#ebf8ff",
                color: "#2c5282",
              },
              ".rdp-chevron": {
                fill: "#4a5568",
              },
              ".rdp-day_disabled": {
                opacity: 0.3,
              },
            }}
          >
            <DayPicker
              mode="single"
              selected={selectedDate}
              onSelect={handleDaySelect}
              locale={es}
              showOutsideDays
              fixedWeeks
            />
          </Box>
        </Portal>
      )}
    </Box>
  )
}
