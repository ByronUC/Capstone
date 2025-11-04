import { useState } from "react"
import { Box, Container, Heading, Text, VStack, SimpleGrid, Icon, Button, HStack, Grid, Card, Badge, Spinner, Input, Textarea } from "@chakra-ui/react"
import { FaInfoCircle, FaMapMarkerAlt, FaSearch, FaClock, FaCheck, FaChevronLeft, FaChevronRight } from "react-icons/fa"
import { useInView } from "react-intersection-observer"
import { Link } from "@tanstack/react-router"
import { useQuery, useMutation } from "@tanstack/react-query"
import { BookingService, type Servicio, type Psicologo } from "../../client/booking"
import { toaster } from "../ui/toaster"

export default function BookingSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })

  // Estados del formulario integrado
  const [step, setStep] = useState(1)
  const [selectedServicio, setSelectedServicio] = useState<Servicio | null>(null)
  const [selectedPsicologo, setSelectedPsicologo] = useState<Psicologo | null>(null)
  const [selectedFecha, setSelectedFecha] = useState<string>("")
  const [selectedHoraInicio, setSelectedHoraInicio] = useState<string>("")
  const [selectedHoraFin, setSelectedHoraFin] = useState<string>("")
  const [mesActual, setMesActual] = useState(new Date())

  // Datos del paciente
  const [rut, setRut] = useState("")
  const [nombres, setNombres] = useState("")
  const [apellidoPaterno, setApellidoPaterno] = useState("")
  const [apellidoMaterno, setApellidoMaterno] = useState("")
  const [telefono, setTelefono] = useState("")
  const [email, setEmail] = useState("")
  const [fechaNacimiento, setFechaNacimiento] = useState("")
  const [motivoConsulta, setMotivoConsulta] = useState("")

  // Estados de validación
  const [rutError, setRutError] = useState("")
  const [emailError, setEmailError] = useState("")

  // Función para validar RUT chileno
  const validarRUT = (rut: string): boolean => {
    // Limpiar el RUT
    const rutLimpio = rut.replace(/[^0-9kK]/g, "")

    if (rutLimpio.length < 2) return false

    const cuerpo = rutLimpio.slice(0, -1)
    const dv = rutLimpio.slice(-1).toUpperCase()

    // Calcular dígito verificador
    let suma = 0
    let multiplo = 2

    for (let i = cuerpo.length - 1; i >= 0; i--) {
      suma += parseInt(cuerpo[i]) * multiplo
      multiplo = multiplo === 7 ? 2 : multiplo + 1
    }

    const dvEsperado = 11 - (suma % 11)
    const dvCalculado = dvEsperado === 11 ? "0" : dvEsperado === 10 ? "K" : dvEsperado.toString()

    return dv === dvCalculado
  }

  // Función para formatear RUT mientras se escribe
  const formatearRUT = (valor: string): string => {
    // Limpiar el valor
    const limpio = valor.replace(/[^0-9kK]/g, "")

    if (limpio.length <= 1) return limpio

    const cuerpo = limpio.slice(0, -1)
    const dv = limpio.slice(-1)

    // Formatear el cuerpo con puntos
    let cuerpoFormateado = ""
    for (let i = cuerpo.length - 1, j = 0; i >= 0; i--, j++) {
      if (j > 0 && j % 3 === 0) cuerpoFormateado = "." + cuerpoFormateado
      cuerpoFormateado = cuerpo[i] + cuerpoFormateado
    }

    return `${cuerpoFormateado}-${dv}`
  }

  // Función para validar email
  const validarEmail = (email: string): boolean => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return regex.test(email)
  }

  // Handler para cambio de RUT
  const handleRutChange = (valor: string) => {
    const formateado = formatearRUT(valor)
    setRut(formateado)

    if (valor.length > 0) {
      if (!validarRUT(valor)) {
        setRutError("RUT inválido")
      } else {
        setRutError("")
      }
    } else {
      setRutError("")
    }
  }

  // Handler para cambio de email
  const handleEmailChange = (valor: string) => {
    setEmail(valor)

    if (valor.length > 0) {
      if (!validarEmail(valor)) {
        setEmailError("Email inválido")
      } else {
        setEmailError("")
      }
    } else {
      setEmailError("")
    }
  }

  // Cargar servicios disponibles
  const { data: servicios, isLoading } = useQuery({
    queryKey: ["servicios-landing"],
    queryFn: BookingService.getServicios,
  })

  // Cargar psicólogos cuando se selecciona un servicio
  const { data: psicologos, isLoading: loadingPsicologos } = useQuery({
    queryKey: ["psicologos-landing", selectedServicio?.id_servicio],
    queryFn: () => BookingService.getPsicologosDisponibles(),
    enabled: !!selectedServicio,
  })

  // Cargar horarios disponibles
  const { data: horariosDisponibles, isLoading: loadingHorarios } = useQuery({
    queryKey: ["disponibilidad-landing", selectedPsicologo?.id_psicologo, selectedFecha],
    queryFn: () =>
      BookingService.getDisponibilidad(
        selectedPsicologo!.id_psicologo,
        selectedFecha,
      ),
    enabled: !!selectedPsicologo && !!selectedFecha,
  })

  // Mutation para crear reserva
  const crearReservaMutation = useMutation({
    mutationFn: BookingService.crearReserva,
    onSuccess: (data) => {
      toaster.create({
        title: "¡Cita reservada exitosamente!",
        description: `Tu código de confirmación es: ${data.codigo_confirmacion}`,
        type: "success",
        duration: 10000,
      })
      // Resetear formulario y volver al paso 1
      setStep(1)
      setSelectedServicio(null)
      setSelectedPsicologo(null)
      setSelectedFecha("")
      setSelectedHoraInicio("")
      setSelectedHoraFin("")
      setRut("")
      setNombres("")
      setApellidoPaterno("")
      setApellidoMaterno("")
      setTelefono("")
      setEmail("")
      setFechaNacimiento("")
      setMotivoConsulta("")
    },
    onError: (error: Error) => {
      toaster.create({
        title: "Error al reservar cita",
        description: error.message,
        type: "error",
      })
    },
  })

  const handleServicioSelect = (servicio: Servicio) => {
    setSelectedServicio(servicio)
    setStep(2)
  }

  const handlePsicologoSelect = (psicologo: Psicologo) => {
    setSelectedPsicologo(psicologo)
    setStep(3)
  }

  const handleHorarioSelect = (hora: string) => {
    setSelectedHoraInicio(hora)
    // Calcular hora fin basado en duración del servicio
    const [h, m] = hora.split(":").map(Number)
    const duracion = selectedServicio?.duracion_minutos || 60
    const totalMinutos = h * 60 + m + duracion
    const horaFin = `${Math.floor(totalMinutos / 60)
      .toString()
      .padStart(2, "0")}:${(totalMinutos % 60).toString().padStart(2, "0")}`
    setSelectedHoraFin(horaFin)
    setStep(4)
  }

  const handleSubmit = () => {
    if (
      !selectedServicio ||
      !selectedPsicologo ||
      !selectedFecha ||
      !selectedHoraInicio
    ) {
      toaster.create({
        title: "Error",
        description: "Por favor completa todos los campos",
        type: "error",
      })
      return
    }

    // Validar RUT
    if (!validarRUT(rut)) {
      toaster.create({
        title: "RUT inválido",
        description: "Por favor ingresa un RUT válido en formato XX.XXX.XXX-X",
        type: "error",
      })
      setRutError("RUT inválido")
      return
    }

    // Validar Email
    if (!validarEmail(email)) {
      toaster.create({
        title: "Email inválido",
        description: "Por favor ingresa un email válido",
        type: "error",
      })
      setEmailError("Email inválido")
      return
    }

    crearReservaMutation.mutate({
      rut,
      nombres,
      apellido_paterno: apellidoPaterno,
      apellido_materno: apellidoMaterno || null,
      telefono,
      email,
      fecha_nacimiento: fechaNacimiento,
      id_servicio: selectedServicio.id_servicio,
      id_psicologo: selectedPsicologo.id_psicologo,
      fecha_cita: selectedFecha,
      hora_inicio: selectedHoraInicio,
      hora_fin: selectedHoraFin,
      motivo_consulta: motivoConsulta || null,
    })
  }

  // Generar fechas disponibles (próximos 60 días desde hoy)
  const getFechasDisponibles = () => {
    const fechas = []
    const hoy = new Date()
    for (let i = 0; i <= 60; i++) {
      const fecha = new Date(hoy)
      fecha.setDate(hoy.getDate() + i)
      fechas.push(fecha.toISOString().split("T")[0])
    }
    return fechas
  }

  return (
    <Box
      id="booking"
      py={{ base: 16, md: 24 }}
      bg="gray.50"
      position="relative"
      ref={ref}
    >
      <Container maxW="1280px">
        <VStack gap={12}>
          <VStack
            gap={4}
            textAlign="center"
            opacity={inView ? 1 : 0}
            transform={inView ? "translateY(0)" : "translateY(30px)"}
            transition="all 0.6s"
          >
            <Heading
              as="h2"
              fontSize={{ base: "3xl", md: "4xl", lg: "5xl" }}
              fontWeight="700"
              color="gray.800"
            >
              Agenda tu Consulta
            </Heading>
            <Text fontSize={{ base: "lg", md: "xl" }} color="gray.600" maxW="800px">
              Da el primer paso hacia tu bienestar
            </Text>

            {/* Botón de acción */}
            <Box mt={4}>
              <Link to="/gestionar-cita">
                <Button
                  size="lg"
                  bg="blue.500"
                  color="white"
                  _hover={{ bg: "blue.600", transform: "translateY(-2px)", shadow: "lg" }}
                  boxShadow="sm"
                >
                  <Icon as={FaSearch} mr={2} />
                  Gestionar mi Cita
                </Button>
              </Link>
            </Box>
          </VStack>

          {/* Formulario de Reserva Integrado */}
          <Box
            w="full"
            maxW="1000px"
            mx="auto"
            opacity={inView ? 1 : 0}
            transform={inView ? "translateY(0)" : "translateY(30px)"}
            transition="all 0.8s 0.2s"
          >
            <Card.Root boxShadow="2xl" borderRadius="2xl" overflow="hidden" bg="white">
              <Card.Body p={{ base: 6, md: 10 }} bg="white">
                {/* Progress Steps */}
                <Box display="flex" justifyContent="center" mb={8}>
                  <HStack justify="space-between" gap={2} maxW="400px" w="full">
                    {[1, 2, 3, 4].map((num) => (
                      <HStack key={num} flex={1}>
                        <Box
                          w="40px"
                          h="40px"
                          borderRadius="full"
                          bg={step >= num ? "blue.500" : "gray.300"}
                          color={step >= num ? "white" : "gray.600"}
                          display="flex"
                          alignItems="center"
                          justifyContent="center"
                          fontWeight="bold"
                          transition="all 0.3s"
                        >
                          {step > num ? <Icon as={FaCheck} /> : num}
                        </Box>
                        {num < 4 && (
                          <Box
                            flex={1}
                            h="2px"
                            bg={step > num ? "blue.500" : "gray.300"}
                            transition="all 0.3s"
                          />
                        )}
                      </HStack>
                    ))}
                  </HStack>
                </Box>

                {/* STEP 1: Seleccionar Servicio */}
                {step === 1 && (
                  <VStack gap={6} align="stretch">
                    <Heading size="lg" textAlign="center" color="gray.800">
                      Selecciona el Servicio
                    </Heading>

                    {isLoading ? (
                      <Box textAlign="center" py={10}>
                        <Spinner size="xl" color="blue.500" />
                      </Box>
                    ) : (
                      <Grid
                        templateColumns={{ base: "1fr", md: "repeat(2, 1fr)" }}
                        gap={4}
                      >
                        {servicios?.map((servicio: Servicio) => (
                          <Card.Root
                            key={servicio.id_servicio}
                            cursor="pointer"
                            onClick={() => handleServicioSelect(servicio)}
                            bg="white"
                            borderWidth={selectedServicio?.id_servicio === servicio.id_servicio ? "3px" : "1px"}
                            borderColor={selectedServicio?.id_servicio === servicio.id_servicio ? "blue.500" : "gray.300"}
                            _hover={{ borderColor: "blue.400", transform: "scale(1.02)", shadow: "md" }}
                            transition="all 0.2s"
                          >
                            <Card.Body p={5} bg="white">
                              <VStack align="start" gap={3}>
                                <Heading size="md" color="gray.800">{servicio.nombre_servicio}</Heading>
                                <Text fontSize="sm" color="gray.600">
                                  {servicio.descripcion}
                                </Text>
                                <HStack gap={2}>
                                  <Badge
                                    bg="green.50"
                                    color="green.700"
                                    px={3}
                                    py={1}
                                    borderRadius="full"
                                    display="flex"
                                    alignItems="center"
                                    gap={1}
                                  >
                                    <Icon as={FaClock} />
                                    {servicio.duracion_minutos} min
                                  </Badge>
                                  <Badge
                                    bg="blue.500"
                                    color="white"
                                    px={3}
                                    py={1}
                                    borderRadius="full"
                                    fontSize="sm"
                                    fontWeight="bold"
                                  >
                                    ${servicio.precio.toLocaleString("es-CL")}
                                  </Badge>
                                </HStack>
                              </VStack>
                            </Card.Body>
                          </Card.Root>
                        ))}
                      </Grid>
                    )}
                  </VStack>
                )}

                {/* STEP 2: Seleccionar Psicólogo */}
                {step === 2 && (
                  <VStack gap={6} align="stretch">
                    <Heading size="lg" textAlign="center" color="gray.800">
                      Selecciona tu Psicólogo
                    </Heading>

                    {loadingPsicologos ? (
                      <Box textAlign="center" py={10}>
                        <Spinner size="xl" color="blue.500" />
                      </Box>
                    ) : (
                      <Grid templateColumns={{ base: "1fr", md: "repeat(2, 1fr)" }} gap={4}>
                        {psicologos?.map((psicologo: Psicologo) => (
                          <Card.Root
                            key={psicologo.id_psicologo}
                            cursor="pointer"
                            onClick={() => handlePsicologoSelect(psicologo)}
                            bg="white"
                            borderWidth={selectedPsicologo?.id_psicologo === psicologo.id_psicologo ? "3px" : "1px"}
                            borderColor={selectedPsicologo?.id_psicologo === psicologo.id_psicologo ? "blue.500" : "gray.300"}
                            _hover={{ borderColor: "blue.400", transform: "scale(1.02)", shadow: "md" }}
                            transition="all 0.2s"
                          >
                            <Card.Body p={5} bg="white">
                              <VStack align="start" gap={3}>
                                <Heading size="md" color="gray.800">
                                  {psicologo.nombres} {psicologo.apellido_paterno}
                                </Heading>
                                <Text fontSize="sm" color="blue.600" fontWeight="medium">
                                  {psicologo.titulo_profesional}
                                </Text>
                                {psicologo.anios_experiencia && (
                                  <Badge
                                    bg="blue.500"
                                    color="white"
                                    px={3}
                                    py={1.5}
                                    borderRadius="full"
                                    fontSize="sm"
                                    fontWeight="bold"
                                  >
                                    {psicologo.anios_experiencia} años de experiencia
                                  </Badge>
                                )}
                              </VStack>
                            </Card.Body>
                          </Card.Root>
                        ))}
                      </Grid>
                    )}

                    <Button
                      onClick={() => setStep(1)}
                      size="lg"
                      bg="gray.600"
                      color="white"
                      _hover={{ bg: "gray.700", transform: "translateY(-2px)", shadow: "md" }}
                      transition="all 0.2s"
                      fontWeight="bold"
                    >
                      Volver
                    </Button>
                  </VStack>
                )}

                {/* STEP 3: Seleccionar Fecha y Hora */}
                {step === 3 && (
                  <VStack gap={6} align="stretch">
                    <Heading size="lg" textAlign="center" color="gray.800">
                      Selecciona Fecha y Hora
                    </Heading>

                    {/* Selector de Fecha - Calendario */}
                    <Box>
                      <HStack justify="space-between" mb={3}>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => {
                            const nuevoMes = new Date(mesActual)
                            nuevoMes.setMonth(mesActual.getMonth() - 1)
                            setMesActual(nuevoMes)
                          }}
                          _hover={{ bg: "blue.50" }}
                        >
                          <Icon as={FaChevronLeft} />
                        </Button>
                        <Text fontWeight="bold" fontSize="lg" color="gray.700">
                          {mesActual.toLocaleDateString("es-CL", { month: "long", year: "numeric" }).charAt(0).toUpperCase() + mesActual.toLocaleDateString("es-CL", { month: "long", year: "numeric" }).slice(1)}
                        </Text>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => {
                            const nuevoMes = new Date(mesActual)
                            nuevoMes.setMonth(mesActual.getMonth() + 1)
                            setMesActual(nuevoMes)
                          }}
                          _hover={{ bg: "blue.50" }}
                        >
                          <Icon as={FaChevronRight} />
                        </Button>
                      </HStack>

                      <Box bg="gray.50" borderRadius="xl" p={5} boxShadow="md" borderWidth="1px" borderColor="gray.200">
                        {/* Días de la semana */}
                        <Grid templateColumns="repeat(7, 1fr)" gap={3} mb={3}>
                          {["D", "L", "M", "M", "J", "V", "S"].map((dia, idx) => (
                            <Box key={idx} textAlign="center" py={2}>
                              <Text fontSize="sm" fontWeight="bold" color="gray.600">
                                {dia}
                              </Text>
                            </Box>
                          ))}
                        </Grid>

                        {/* Grid de días */}
                        <Grid templateColumns="repeat(7, 1fr)" gap={2}>
                          {(() => {
                            const hoy = new Date()
                            const primerDia = new Date(mesActual.getFullYear(), mesActual.getMonth(), 1)
                            const ultimoDia = new Date(mesActual.getFullYear(), mesActual.getMonth() + 1, 0)
                            const diasMesAnterior = primerDia.getDay()
                            const diasMes = ultimoDia.getDate()

                            const dias = []

                            // Días del mes anterior (grises)
                            const ultimoDiaMesAnterior = new Date(mesActual.getFullYear(), mesActual.getMonth(), 0).getDate()
                            for (let i = diasMesAnterior - 1; i >= 0; i--) {
                              dias.push(
                                <Box
                                  key={`prev-${i}`}
                                  textAlign="center"
                                  py={3}
                                  display="flex"
                                  alignItems="center"
                                  justifyContent="center"
                                >
                                  <Text fontSize="sm" color="gray.400" fontWeight="medium">
                                    {ultimoDiaMesAnterior - i}
                                  </Text>
                                </Box>
                              )
                            }

                            // Días del mes actual
                            const fechasDisponibles = getFechasDisponibles()
                            for (let dia = 1; dia <= diasMes; dia++) {
                              const fechaStr = `${mesActual.getFullYear()}-${String(mesActual.getMonth() + 1).padStart(2, '0')}-${String(dia).padStart(2, '0')}`
                              const esHoy = dia === hoy.getDate() && mesActual.getMonth() === hoy.getMonth() && mesActual.getFullYear() === hoy.getFullYear()
                              const estaSeleccionado = selectedFecha === fechaStr
                              const estaDisponible = fechasDisponibles.includes(fechaStr)

                              dias.push(
                                <Box
                                  key={dia}
                                  display="flex"
                                  alignItems="center"
                                  justifyContent="center"
                                  h="45px"
                                  borderRadius="lg"
                                  cursor={estaDisponible ? "pointer" : "default"}
                                  bg={estaSeleccionado ? "blue.500" : esHoy ? "blue.100" : "transparent"}
                                  color={estaSeleccionado ? "white" : esHoy ? "blue.600" : estaDisponible ? "gray.800" : "gray.400"}
                                  borderWidth={esHoy && !estaSeleccionado ? "2px" : "0"}
                                  borderColor={esHoy && !estaSeleccionado ? "blue.500" : "transparent"}
                                  _hover={estaDisponible ? {
                                    bg: estaSeleccionado ? "blue.600" : "blue.50",
                                    transform: "scale(1.05)",
                                    shadow: "md"
                                  } : {}}
                                  transition="all 0.2s"
                                  onClick={() => estaDisponible && setSelectedFecha(fechaStr)}
                                  fontWeight={estaSeleccionado || esHoy || estaDisponible ? "bold" : "medium"}
                                  fontSize="md"
                                >
                                  {dia}
                                </Box>
                              )
                            }

                            // Días del siguiente mes (grises)
                            const diasRestantes = 42 - dias.length // 6 semanas × 7 días
                            for (let i = 1; i <= diasRestantes; i++) {
                              dias.push(
                                <Box
                                  key={`next-${i}`}
                                  textAlign="center"
                                  py={3}
                                  display="flex"
                                  alignItems="center"
                                  justifyContent="center"
                                >
                                  <Text fontSize="sm" color="gray.400" fontWeight="medium">
                                    {i}
                                  </Text>
                                </Box>
                              )
                            }

                            return dias
                          })()}
                        </Grid>
                      </Box>
                    </Box>

                    {/* Selector de Hora */}
                    {selectedFecha && (
                      <Box>
                        <Text fontWeight="bold" mb={3} fontSize="lg" color="gray.700">
                          Horarios disponibles:
                        </Text>

                        {loadingHorarios ? (
                          <Box textAlign="center" py={6}>
                            <Spinner color="blue.500" />
                          </Box>
                        ) : horariosDisponibles && horariosDisponibles.length > 0 ? (
                          <Grid templateColumns="repeat(auto-fill, minmax(110px, 1fr))" gap={3}>
                            {horariosDisponibles.map((horarioInfo: any) => {
                              const { hora, disponible, ocupado, pasado } = horarioInfo

                              // Determinar si está deshabilitado
                              const isDisabled = ocupado || pasado
                              const tooltip = ocupado ? "Horario ocupado" : pasado ? "Horario pasado" : ""

                              return (
                                <Button
                                  key={hora}
                                  onClick={() => !isDisabled && handleHorarioSelect(hora)}
                                  size="lg"
                                  h="60px"
                                  bg={selectedHoraInicio === hora ? "blue.500" : ocupado ? "red.50" : pasado ? "gray.100" : "white"}
                                  color={selectedHoraInicio === hora ? "white" : ocupado ? "red.600" : pasado ? "gray.500" : "gray.700"}
                                  borderWidth="2px"
                                  borderColor={selectedHoraInicio === hora ? "blue.500" : ocupado ? "red.300" : pasado ? "gray.300" : "gray.300"}
                                  fontSize="xl"
                                  fontWeight="bold"
                                  boxShadow="sm"
                                  disabled={isDisabled}
                                  cursor={isDisabled ? "not-allowed" : "pointer"}
                                  opacity={isDisabled ? 0.6 : 1}
                                  title={tooltip}
                                  _hover={isDisabled ? {} : {
                                    bg: selectedHoraInicio === hora ? "blue.600" : "blue.50",
                                    borderColor: "blue.500",
                                    transform: "translateY(-2px)",
                                    shadow: "lg"
                                  }}
                                  transition="all 0.2s"
                                >
                                  {hora}
                                  {ocupado && " 🔒"}
                                  {pasado && " ⏰"}
                                </Button>
                              )
                            })}
                          </Grid>
                        ) : (
                          <Text color="gray.500" textAlign="center" py={4}>
                            No hay horarios disponibles para esta fecha
                          </Text>
                        )}
                      </Box>
                    )}

                    <Button
                      onClick={() => setStep(2)}
                      size="lg"
                      bg="gray.600"
                      color="white"
                      _hover={{ bg: "gray.700", transform: "translateY(-2px)", shadow: "md" }}
                      transition="all 0.2s"
                      fontWeight="bold"
                    >
                      Volver
                    </Button>
                  </VStack>
                )}

                {/* STEP 4: Datos del Paciente */}
                {step === 4 && (
                  <VStack gap={6} align="stretch">
                    <Heading size="lg" textAlign="center" color="gray.800">
                      Completa tus Datos
                    </Heading>

                    <Grid templateColumns={{ base: "1fr", md: "repeat(2, 1fr)" }} gap={4}>
                      <Box>
                        <Text fontWeight="semibold" mb={2} color="gray.700">
                          RUT <Text as="span" color="red.500">*</Text>
                        </Text>
                        <Input
                          placeholder="12.345.678-9"
                          value={rut}
                          onChange={(e) => handleRutChange(e.target.value)}
                          size="lg"
                          bg="white"
                          borderColor={rutError ? "red.500" : "gray.300"}
                          _hover={{ borderColor: rutError ? "red.600" : "blue.400" }}
                          _focus={{ borderColor: rutError ? "red.500" : "blue.500", boxShadow: rutError ? "0 0 0 1px var(--chakra-colors-red-500)" : "0 0 0 1px var(--chakra-colors-blue-500)" }}
                        />
                        {rutError && (
                          <Text color="red.500" fontSize="sm" mt={1}>
                            {rutError}
                          </Text>
                        )}
                      </Box>

                      <Box>
                        <Text fontWeight="semibold" mb={2} color="gray.700">
                          Nombres <Text as="span" color="red.500">*</Text>
                        </Text>
                        <Input
                          placeholder="Juan Carlos"
                          value={nombres}
                          onChange={(e) => setNombres(e.target.value)}
                          size="lg"
                          bg="white"
                          borderColor="gray.300"
                          _hover={{ borderColor: "blue.400" }}
                          _focus={{ borderColor: "blue.500", boxShadow: "0 0 0 1px var(--chakra-colors-blue-500)" }}
                        />
                      </Box>

                      <Box>
                        <Text fontWeight="semibold" mb={2} color="gray.700">
                          Apellido Paterno <Text as="span" color="red.500">*</Text>
                        </Text>
                        <Input
                          placeholder="González"
                          value={apellidoPaterno}
                          onChange={(e) => setApellidoPaterno(e.target.value)}
                          size="lg"
                          bg="white"
                          borderColor="gray.300"
                          _hover={{ borderColor: "blue.400" }}
                          _focus={{ borderColor: "blue.500", boxShadow: "0 0 0 1px var(--chakra-colors-blue-500)" }}
                        />
                      </Box>

                      <Box>
                        <Text fontWeight="semibold" mb={2} color="gray.700">
                          Apellido Materno
                        </Text>
                        <Input
                          placeholder="López"
                          value={apellidoMaterno}
                          onChange={(e) => setApellidoMaterno(e.target.value)}
                          size="lg"
                          bg="white"
                          borderColor="gray.300"
                          _hover={{ borderColor: "blue.400" }}
                          _focus={{ borderColor: "blue.500", boxShadow: "0 0 0 1px var(--chakra-colors-blue-500)" }}
                        />
                      </Box>

                      <Box>
                        <Text fontWeight="semibold" mb={2} color="gray.700">
                          Teléfono <Text as="span" color="red.500">*</Text>
                        </Text>
                        <Input
                          placeholder="+56912345678"
                          value={telefono}
                          onChange={(e) => setTelefono(e.target.value)}
                          size="lg"
                          bg="white"
                          borderColor="gray.300"
                          _hover={{ borderColor: "blue.400" }}
                          _focus={{ borderColor: "blue.500", boxShadow: "0 0 0 1px var(--chakra-colors-blue-500)" }}
                        />
                      </Box>

                      <Box>
                        <Text fontWeight="semibold" mb={2} color="gray.700">
                          Email <Text as="span" color="red.500">*</Text>
                        </Text>
                        <Input
                          type="email"
                          placeholder="tu@email.com"
                          value={email}
                          onChange={(e) => handleEmailChange(e.target.value)}
                          size="lg"
                          bg="white"
                          borderColor={emailError ? "red.500" : "gray.300"}
                          _hover={{ borderColor: emailError ? "red.600" : "blue.400" }}
                          _focus={{ borderColor: emailError ? "red.500" : "blue.500", boxShadow: emailError ? "0 0 0 1px var(--chakra-colors-red-500)" : "0 0 0 1px var(--chakra-colors-blue-500)" }}
                        />
                        {emailError && (
                          <Text color="red.500" fontSize="sm" mt={1}>
                            {emailError}
                          </Text>
                        )}
                      </Box>

                      <Box>
                        <Text fontWeight="semibold" mb={2} color="gray.700">
                          Fecha de Nacimiento <Text as="span" color="red.500">*</Text>
                        </Text>
                        <Input
                          type="date"
                          value={fechaNacimiento}
                          onChange={(e) => setFechaNacimiento(e.target.value)}
                          size="lg"
                          bg="white"
                          borderColor="gray.300"
                          _hover={{ borderColor: "blue.400" }}
                          _focus={{ borderColor: "blue.500", boxShadow: "0 0 0 1px var(--chakra-colors-blue-500)" }}
                          fontWeight="500"
                          css={{
                            colorScheme: "light",
                            "&::-webkit-calendar-picker-indicator": {
                              cursor: "pointer",
                              borderRadius: "4px",
                              padding: "4px",
                              filter: "invert(0.5) sepia(1) saturate(5) hue-rotate(175deg)",
                              transition: "all 0.2s",
                            },
                            "&::-webkit-calendar-picker-indicator:hover": {
                              filter: "invert(0.4) sepia(1) saturate(6) hue-rotate(175deg)",
                              transform: "scale(1.1)",
                            }
                          }}
                        />
                      </Box>
                    </Grid>

                    <Box>
                      <Text fontWeight="semibold" mb={2} color="gray.700">
                        Motivo de Consulta
                      </Text>
                      <Textarea
                        placeholder="Describe brevemente el motivo de tu consulta..."
                        value={motivoConsulta}
                        onChange={(e) => setMotivoConsulta(e.target.value)}
                        rows={3}
                        bg="white"
                        borderColor="gray.300"
                        _hover={{ borderColor: "blue.400" }}
                        _focus={{ borderColor: "blue.500", boxShadow: "0 0 0 1px var(--chakra-colors-blue-500)" }}
                      />
                    </Box>

                    {/* Resumen */}
                    <Box p={5} bg="white" borderRadius="lg" borderWidth="2px" borderColor="blue.300" boxShadow="sm">
                      <Heading size="sm" mb={3} color="blue.600">
                        Resumen de tu Reserva:
                      </Heading>
                      <VStack align="start" gap={2} fontSize="sm" color="gray.700">
                        <Text>
                          <strong>Servicio:</strong> {selectedServicio?.nombre_servicio}
                        </Text>
                        <Text>
                          <strong>Psicólogo:</strong> {selectedPsicologo?.nombres}{" "}
                          {selectedPsicologo?.apellido_paterno}
                        </Text>
                        <Text>
                          <strong>Fecha:</strong> {selectedFecha}
                        </Text>
                        <Text>
                          <strong>Hora:</strong> {selectedHoraInicio}
                        </Text>
                        <Text>
                          <strong>Precio:</strong> ${selectedServicio?.precio.toLocaleString("es-CL")}
                        </Text>
                      </VStack>
                    </Box>

                    <HStack gap={3}>
                      <Button
                        onClick={() => setStep(3)}
                        flex={1}
                        size="lg"
                        bg="gray.600"
                        color="white"
                        _hover={{ bg: "gray.700", transform: "translateY(-2px)", shadow: "md" }}
                        transition="all 0.2s"
                        fontWeight="bold"
                      >
                        Volver
                      </Button>
                      <Button
                        onClick={handleSubmit}
                        flex={1}
                        size="lg"
                        bg="blue.500"
                        color="white"
                        _hover={{ bg: "blue.600", transform: "translateY(-2px)", shadow: "lg" }}
                        transition="all 0.2s"
                        loading={crearReservaMutation.isPending}
                        fontWeight="bold"
                      >
                        Confirmar Reserva
                      </Button>
                    </HStack>
                  </VStack>
                )}
              </Card.Body>
            </Card.Root>
          </Box>

          <SimpleGrid columns={{ base: 1, md: 2 }} gap={8} w="full" maxW="900px">
            <Box
              bg="white"
              p={8}
              borderRadius="xl"
              boxShadow="lg"
              opacity={inView ? 1 : 0}
              transition="all 0.8s 0.3s"
            >
              <VStack align="start" gap={3}>
                <Box
                  bg="rgba(66, 133, 244, 0.1)"
                  p={3}
                  borderRadius="lg"
                  display="inline-flex"
                >
                  <Icon as={FaInfoCircle} fontSize="2xl" color="#4285F4" />
                </Box>
                <Heading as="h3" fontSize="xl" color="gray.800">
                  ¿Cómo funciona?
                </Heading>
                <Text fontSize="md" color="gray.700" lineHeight="1.8">
                  Selecciona el día y horario que mejor te acomode. Recibirás un correo de confirmación con los detalles de tu cita y un recordatorio 24 horas antes.
                </Text>
              </VStack>
            </Box>

            <Box
              bg="white"
              p={8}
              borderRadius="xl"
              boxShadow="lg"
              opacity={inView ? 1 : 0}
              transition="all 0.8s 0.4s"
            >
              <VStack align="start" gap={3}>
                <Box
                  bg="rgba(66, 133, 244, 0.1)"
                  p={3}
                  borderRadius="lg"
                  display="inline-flex"
                >
                  <Icon as={FaMapMarkerAlt} fontSize="2xl" color="#4285F4" />
                </Box>
                <Heading as="h3" fontSize="xl" color="gray.800">
                  Modalidades de atención
                </Heading>
                <Text fontSize="md" color="gray.700" lineHeight="1.8">
                  Ofrecemos sesiones presenciales en nuestra oficina de Santiago Centro y también sesiones online vía Zoom o Google Meet según tu preferencia.
                </Text>
              </VStack>
            </Box>
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  )
}
