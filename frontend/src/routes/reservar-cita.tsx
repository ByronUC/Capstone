import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useMutation, useQuery } from "@tanstack/react-query"
import { useState } from "react"
import {
  Box,
  Container,
  Heading,
  VStack,
  HStack,
  Button,
  Input,
  Textarea,
  Text,
  Grid,
  Card,
  Badge,
  Spinner,
  Alert,
} from "@chakra-ui/react"
import { Field } from "../components/ui/field"
import { toaster } from "../components/ui/toaster"
import { Stepper, useSteps } from "../components/ui/stepper"
import { BookingService, type Servicio, type Psicologo } from "../client/booking"
import LandingNavbar from "../components/Landing/LandingNavbar"
import LandingFooter from "../components/Landing/LandingFooter"

export const Route = createFileRoute("/reservar-cita")({
  component: ReservarCitaPage,
})

const steps = [
  { title: "Servicio", description: "Selecciona el servicio" },
  { title: "Profesional", description: "Elige tu psicólogo" },
  { title: "Fecha y Hora", description: "Selecciona cuando" },
  { title: "Datos", description: "Completa tus datos" },
]

function ReservarCitaPage() {
  const navigate = useNavigate()
  const { activeStep, goToNext, goToPrevious, setActiveStep } = useSteps({
    index: 0,
    count: steps.length,
  })

  // Estados del formulario
  const [selectedServicio, setSelectedServicio] = useState<Servicio | null>(null)
  const [selectedPsicologo, setSelectedPsicologo] = useState<Psicologo | null>(null)
  const [selectedFecha, setSelectedFecha] = useState<string>("")
  const [selectedHoraInicio, setSelectedHoraInicio] = useState<string>("")
  const [selectedHoraFin, setSelectedHoraFin] = useState<string>("")

  // Datos del paciente
  const [rut, setRut] = useState("")
  const [nombres, setNombres] = useState("")
  const [apellidoPaterno, setApellidoPaterno] = useState("")
  const [apellidoMaterno, setApellidoMaterno] = useState("")
  const [telefono, setTelefono] = useState("")
  const [email, setEmail] = useState("")
  const [fechaNacimiento, setFechaNacimiento] = useState("")
  const [motivoConsulta, setMotivoConsulta] = useState("")

  // Queries
  const { data: servicios, isLoading: loadingServicios } = useQuery({
    queryKey: ["servicios"],
    queryFn: BookingService.getServicios,
  })

  const { data: psicologos, isLoading: loadingPsicologos } = useQuery({
    queryKey: ["psicologos", selectedServicio?.id_servicio],
    queryFn: () => BookingService.getPsicologosDisponibles(),
    enabled: !!selectedServicio,
  })

  const { data: horariosDisponibles, isLoading: loadingHorarios } = useQuery({
    queryKey: ["disponibilidad", selectedPsicologo?.id_psicologo, selectedFecha],
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
      // Navegar a página de confirmación
      navigate({
        to: "/confirmacion-cita",
        search: { codigo: data.codigo_confirmacion },
      })
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
    goToNext()
  }

  const handlePsicologoSelect = (psicologo: Psicologo) => {
    setSelectedPsicologo(psicologo)
    goToNext()
  }

  const handleHorarioSelect = (hora: string, disponible: boolean) => {
    // No permitir seleccionar horarios no disponibles
    if (!disponible) return

    setSelectedHoraInicio(hora)
    // Calcular hora fin basado en duración del servicio
    const [h, m] = hora.split(":").map(Number)
    const duracion = selectedServicio?.duracion_minutos || 60
    const totalMinutos = h * 60 + m + duracion
    const horaFin = `${Math.floor(totalMinutos / 60)
      .toString()
      .padStart(2, "0")}:${(totalMinutos % 60).toString().padStart(2, "0")}`
    setSelectedHoraFin(horaFin)
    goToNext()
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

  // Generar fechas disponibles (próximos 30 días)
  const getFechasDisponibles = () => {
    const fechas = []
    const hoy = new Date()
    for (let i = 1; i <= 30; i++) {
      const fecha = new Date(hoy)
      fecha.setDate(hoy.getDate() + i)
      fechas.push(fecha.toISOString().split("T")[0])
    }
    return fechas
  }

  return (
    <Box minH="100vh" bg="gray.50">
      <LandingNavbar />

      <Container maxW="container.xl" py={10}>
        <VStack gap={8} align="stretch">
          {/* Header */}
          <Box textAlign="center">
            <Heading size="2xl" mb={2}>
              Reserva tu Cita
            </Heading>
            <Text color="gray.600">
              Agenda tu sesión de forma rápida y sencilla
            </Text>
          </Box>

          {/* Stepper */}
          <Stepper steps={steps} activeStep={activeStep} colorScheme="teal" />

          {/* Step Content */}
          <Card.Root>
            <Card.Body p={8}>
              {/* STEP 1: Seleccionar Servicio */}
              {activeStep === 0 && (
                <VStack gap={4} align="stretch">
                  <Heading size="lg" mb={4}>
                    Selecciona el Servicio
                  </Heading>

                  {loadingServicios ? (
                    <Box textAlign="center" py={8}>
                      <Spinner size="xl" />
                    </Box>
                  ) : (
                    <Grid templateColumns="repeat(auto-fit, minmax(250px, 1fr))" gap={4}>
                      {servicios?.map((servicio) => (
                        <Card.Root
                          key={servicio.id_servicio}
                          cursor="pointer"
                          onClick={() => handleServicioSelect(servicio)}
                          borderWidth={
                            selectedServicio?.id_servicio === servicio.id_servicio
                              ? "2px"
                              : "1px"
                          }
                          borderColor={
                            selectedServicio?.id_servicio === servicio.id_servicio
                              ? "teal.500"
                              : "gray.200"
                          }
                          _hover={{ borderColor: "teal.300", shadow: "md" }}
                        >
                          <Card.Body>
                            <VStack align="start" gap={2}>
                              <Heading size="md">{servicio.nombre_servicio}</Heading>
                              <Text fontSize="sm" color="gray.600">
                                {servicio.descripcion}
                              </Text>
                              <HStack>
                                <Badge colorScheme="blue">
                                  {servicio.duracion_minutos} min
                                </Badge>
                                <Badge colorScheme="green">
                                  ${servicio.precio.toLocaleString()}
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
              {activeStep === 1 && (
                <VStack gap={4} align="stretch">
                  <Heading size="lg" mb={4}>
                    Selecciona tu Psicólogo
                  </Heading>

                  {loadingPsicologos ? (
                    <Box textAlign="center" py={8}>
                      <Spinner size="xl" />
                    </Box>
                  ) : (
                    <Grid templateColumns="repeat(auto-fit, minmax(280px, 1fr))" gap={4}>
                      {psicologos?.map((psicologo) => (
                        <Card.Root
                          key={psicologo.id_psicologo}
                          cursor="pointer"
                          onClick={() => handlePsicologoSelect(psicologo)}
                          borderWidth={
                            selectedPsicologo?.id_psicologo ===
                            psicologo.id_psicologo
                              ? "2px"
                              : "1px"
                          }
                          borderColor={
                            selectedPsicologo?.id_psicologo ===
                            psicologo.id_psicologo
                              ? "teal.500"
                              : "gray.200"
                          }
                          _hover={{ borderColor: "teal.300", shadow: "md" }}
                        >
                          <Card.Body>
                            <VStack align="start" gap={2}>
                              <Heading size="md">
                                {psicologo.nombres} {psicologo.apellido_paterno}
                              </Heading>
                              <Text fontSize="sm" color="gray.600">
                                {psicologo.titulo_profesional}
                              </Text>
                              {psicologo.anios_experiencia && (
                                <Badge colorScheme="purple">
                                  {psicologo.anios_experiencia} años de experiencia
                                </Badge>
                              )}
                            </VStack>
                          </Card.Body>
                        </Card.Root>
                      ))}
                    </Grid>
                  )}

                  <Button onClick={goToPrevious} variant="outline">
                    Volver
                  </Button>
                </VStack>
              )}

              {/* STEP 3: Seleccionar Fecha y Hora */}
              {activeStep === 2 && (
                <VStack gap={6} align="stretch">
                  <Heading size="lg" mb={4}>
                    Selecciona Fecha y Hora
                  </Heading>

                  {/* Selector de Fecha */}
                  <Box>
                    <Text fontWeight="bold" mb={2}>
                      Selecciona una fecha:
                    </Text>
                    <Grid templateColumns="repeat(auto-fill, minmax(100px, 1fr))" gap={2}>
                      {getFechasDisponibles().map((fecha) => {
                        const fechaObj = new Date(fecha + "T12:00:00")
                        const dia = fechaObj.getDate()
                        const mes = fechaObj.toLocaleDateString("es-CL", {
                          month: "short",
                        })

                        return (
                          <Button
                            key={fecha}
                            onClick={() => setSelectedFecha(fecha)}
                            variant={selectedFecha === fecha ? "solid" : "outline"}
                            colorScheme={selectedFecha === fecha ? "teal" : "gray"}
                            h="auto"
                            py={3}
                          >
                            <VStack gap={0}>
                              <Text fontSize="xs">{mes}</Text>
                              <Text fontSize="xl" fontWeight="bold">
                                {dia}
                              </Text>
                            </VStack>
                          </Button>
                        )
                      })}
                    </Grid>
                  </Box>

                  {/* Selector de Hora */}
                  {selectedFecha && (
                    <Box>
                      <Text fontWeight="bold" mb={2}>
                        Horarios disponibles:
                      </Text>

                      {loadingHorarios ? (
                        <Box textAlign="center" py={4}>
                          <Spinner />
                        </Box>
                      ) : horariosDisponibles && horariosDisponibles.length > 0 ? (
                        <Grid templateColumns="repeat(auto-fill, minmax(100px, 1fr))" gap={2}>
                          {horariosDisponibles.map((horarioInfo) => {
                            const { hora, disponible, ocupado, pasado } = horarioInfo

                            // Determinar el estado visual
                            let colorScheme = "teal"
                            let variant: "outline" | "solid" | "subtle" = "outline"
                            let isDisabled = false
                            let tooltip = ""

                            if (ocupado) {
                              colorScheme = "red"
                              variant = "subtle"
                              isDisabled = true
                              tooltip = "Horario ocupado"
                            } else if (pasado) {
                              colorScheme = "gray"
                              variant = "subtle"
                              isDisabled = true
                              tooltip = "Horario pasado"
                            }

                            return (
                              <Button
                                key={hora}
                                onClick={() => handleHorarioSelect(hora, disponible)}
                                variant={variant}
                                colorScheme={colorScheme}
                                disabled={isDisabled}
                                cursor={isDisabled ? "not-allowed" : "pointer"}
                                opacity={isDisabled ? 0.6 : 1}
                                title={tooltip}
                                _hover={isDisabled ? {} : { borderColor: "teal.500" }}
                              >
                                {hora}
                                {ocupado && " 🔒"}
                                {pasado && " ⏰"}
                              </Button>
                            )
                          })}
                        </Grid>
                      ) : (
                        <Alert.Root status="info">
                          <Alert.Indicator />
                          <Alert.Title>No hay horarios disponibles</Alert.Title>
                          <Alert.Description>
                            Por favor selecciona otra fecha
                          </Alert.Description>
                        </Alert.Root>
                      )}
                    </Box>
                  )}

                  <Button onClick={goToPrevious} variant="outline">
                    Volver
                  </Button>
                </VStack>
              )}

              {/* STEP 4: Datos del Paciente */}
              {activeStep === 3 && (
                <VStack gap={4} align="stretch">
                  <Heading size="lg" mb={4}>
                    Completa tus Datos
                  </Heading>

                  <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                    <Field label="RUT" required>
                      <Input
                        placeholder="12.345.678-9"
                        value={rut}
                        onChange={(e) => setRut(e.target.value)}
                      />
                    </Field>

                    <Field label="Nombres" required>
                      <Input
                        placeholder="Juan Carlos"
                        value={nombres}
                        onChange={(e) => setNombres(e.target.value)}
                      />
                    </Field>

                    <Field label="Apellido Paterno" required>
                      <Input
                        placeholder="González"
                        value={apellidoPaterno}
                        onChange={(e) => setApellidoPaterno(e.target.value)}
                      />
                    </Field>

                    <Field label="Apellido Materno">
                      <Input
                        placeholder="López"
                        value={apellidoMaterno}
                        onChange={(e) => setApellidoMaterno(e.target.value)}
                      />
                    </Field>

                    <Field label="Teléfono" required>
                      <Input
                        placeholder="+56912345678"
                        value={telefono}
                        onChange={(e) => setTelefono(e.target.value)}
                      />
                    </Field>

                    <Field label="Email" required>
                      <Input
                        type="email"
                        placeholder="tu@email.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                      />
                    </Field>

                    <Field label="Fecha de Nacimiento" required>
                      <Input
                        type="date"
                        value={fechaNacimiento}
                        onChange={(e) => setFechaNacimiento(e.target.value)}
                      />
                    </Field>
                  </Grid>

                  <Field label="Motivo de Consulta">
                    <Textarea
                      placeholder="Describe brevemente el motivo de tu consulta..."
                      value={motivoConsulta}
                      onChange={(e) => setMotivoConsulta(e.target.value)}
                      rows={4}
                    />
                  </Field>

                  {/* Resumen */}
                  <Box p={4} bg="gray.100" borderRadius="md">
                    <Heading size="sm" mb={2}>
                      Resumen de tu Reserva:
                    </Heading>
                    <VStack align="start" gap={1}>
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
                        <strong>Precio:</strong> ${selectedServicio?.precio.toLocaleString()}
                      </Text>
                    </VStack>
                  </Box>

                  <HStack>
                    <Button onClick={goToPrevious} variant="outline" flex={1}>
                      Volver
                    </Button>
                    <Button
                      onClick={handleSubmit}
                      colorScheme="teal"
                      flex={1}
                      loading={crearReservaMutation.isPending}
                    >
                      Confirmar Reserva
                    </Button>
                  </HStack>
                </VStack>
              )}
            </Card.Body>
          </Card.Root>
        </VStack>
      </Container>

      <LandingFooter />
    </Box>
  )
}
