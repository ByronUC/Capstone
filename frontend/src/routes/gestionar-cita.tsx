import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { useMutation, useQuery } from "@tanstack/react-query"
import {
  Box,
  Container,
  Heading,
  VStack,
  HStack,
  Button,
  Input,
  Text,
  Card,
  Badge,
  Spinner,
  Alert,
  Grid,
} from "@chakra-ui/react"
import { Field } from "../components/ui/field"
import { toaster } from "../components/ui/toaster"
import {
  DialogActionTrigger,
  DialogBody,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
} from "../components/ui/dialog"
import { BookingService, type Cita } from "../client/booking"
import LandingNavbar from "../components/Landing/LandingNavbar"
import LandingFooter from "../components/Landing/LandingFooter"

export const Route = createFileRoute("/gestionar-cita")({
  component: GestionarCitaPage,
})

function GestionarCitaPage() {
  const [codigoConfirmacion, setCodigoConfirmacion] = useState("")
  const [citaBuscada, setCitaBuscada] = useState<Cita | null>(null)
  const [buscando, setBuscando] = useState(false)

  // Estados para reagendar
  const [reagendando, setReagendando] = useState(false)
  const [nuevaFecha, setNuevaFecha] = useState("")
  const [nuevaHora, setNuevaHora] = useState("")

  // Mutation para cancelar
  const cancelarMutation = useMutation({
    mutationFn: (codigo: string) => BookingService.cancelarCita(codigo),
    onSuccess: () => {
      toaster.create({
        title: "Cita cancelada",
        description: "Tu cita ha sido cancelada exitosamente",
        type: "success",
      })
      setCitaBuscada(null)
      setCodigoConfirmacion("")
    },
    onError: (error: Error) => {
      toaster.create({
        title: "Error al cancelar",
        description: error.message,
        type: "error",
      })
    },
  })

  // Mutation para reagendar
  const reagendarMutation = useMutation({
    mutationFn: ({ codigo, fecha, hora }: { codigo: string; fecha: string; hora: string }) => {
      const [h, m] = hora.split(":")
      const duracion = 60 // Asumimos 60 minutos
      const totalMinutos = parseInt(h) * 60 + parseInt(m) + duracion
      const horaFin = `${Math.floor(totalMinutos / 60).toString().padStart(2, "0")}:${(totalMinutos % 60).toString().padStart(2, "0")}`

      return BookingService.reagendarCita(codigo, {
        nueva_fecha: fecha,
        nueva_hora_inicio: hora,
        nueva_hora_fin: horaFin,
      })
    },
    onSuccess: (data) => {
      toaster.create({
        title: "Cita reagendada",
        description: `Tu cita ha sido reagendada para el ${data.nueva_fecha} a las ${data.nueva_hora_inicio}`,
        type: "success",
      })
      setReagendando(false)
      setCitaBuscada(null)
      setCodigoConfirmacion("")
    },
    onError: (error: Error) => {
      toaster.create({
        title: "Error al reagendar",
        description: error.message,
        type: "error",
      })
    },
  })

  const buscarCita = async () => {
    if (!codigoConfirmacion.trim()) {
      toaster.create({
        title: "Código requerido",
        description: "Por favor ingresa tu código de confirmación",
        type: "error",
      })
      return
    }

    setBuscando(true)
    try {
      const cita = await BookingService.getCitaPorCodigo(codigoConfirmacion.trim())
      setCitaBuscada(cita)
    } catch (error) {
      toaster.create({
        title: "Cita no encontrada",
        description:
          error instanceof Error ? error.message : "Verifica tu código e intenta nuevamente",
        type: "error",
      })
      setCitaBuscada(null)
    } finally {
      setBuscando(false)
    }
  }

  const handleCancelar = () => {
    if (citaBuscada?.codigo_confirmacion) {
      cancelarMutation.mutate(citaBuscada.codigo_confirmacion)
    }
  }

  const handleReagendar = () => {
    if (!nuevaFecha || !nuevaHora) {
      toaster.create({
        title: "Datos incompletos",
        description: "Por favor selecciona fecha y hora",
        type: "error",
      })
      return
    }

    if (citaBuscada?.codigo_confirmacion) {
      reagendarMutation.mutate({
        codigo: citaBuscada.codigo_confirmacion,
        fecha: nuevaFecha,
        hora: nuevaHora,
      })
    }
  }

  const getEstadoColor = (estadoId: number) => {
    const estados: Record<number, string> = {
      1: "yellow",
      2: "green",
      3: "blue",
      4: "orange",
      5: "red",
    }
    return estados[estadoId] || "gray"
  }

  const getEstadoNombre = (estadoId: number) => {
    const estados: Record<number, string> = {
      1: "Pendiente",
      2: "Confirmada",
      3: "Realizada",
      4: "Reprogramada",
      5: "Cancelada",
    }
    return estados[estadoId] || "Desconocido"
  }

  // Generar horarios (9:00 - 18:00)
  const generarHorarios = () => {
    const horarios = []
    for (let h = 9; h <= 18; h++) {
      horarios.push(`${h.toString().padStart(2, "0")}:00`)
    }
    return horarios
  }

  return (
    <Box minH="100vh" bg="gray.50">
      <LandingNavbar />

      <Container maxW="container.md" py={10}>
        <VStack gap={8} align="stretch">
          {/* Header */}
          <Box textAlign="center">
            <Heading size="2xl" mb={2}>
              Gestionar mi Cita
            </Heading>
            <Text color="gray.600">
              Ingresa tu código de confirmación para ver, reagendar o cancelar tu cita
            </Text>
          </Box>

          {/* Buscar Cita */}
          <Card.Root boxShadow="lg">
            <Card.Body p={5}>
              <VStack gap={3}>
                <Box w="full">
                  <Text fontWeight="semibold" mb={2} color="gray.700">
                    Código de Confirmación <Text as="span" color="red.500">*</Text>
                  </Text>
                  <Input
                    placeholder="Ej: A3B7C9D2"
                    value={codigoConfirmacion}
                    onChange={(e) => setCodigoConfirmacion(e.target.value.toUpperCase())}
                    size="lg"
                    textAlign="center"
                    fontFamily="mono"
                    letterSpacing="wider"
                    bg="white"
                    borderColor="gray.300"
                    _hover={{ borderColor: "blue.400" }}
                    _focus={{ borderColor: "blue.500", boxShadow: "0 0 0 1px var(--chakra-colors-blue-500)" }}
                  />
                </Box>

                <Button
                  bg="blue.500"
                  color="white"
                  _hover={{ bg: "blue.600", transform: "translateY(-2px)", shadow: "lg" }}
                  size="md"
                  w="full"
                  onClick={buscarCita}
                  loading={buscando}
                  fontWeight="bold"
                  boxShadow="sm"
                >
                  Buscar mi Cita
                </Button>
              </VStack>
            </Card.Body>
          </Card.Root>

          {/* Información de la Cita */}
          {citaBuscada && (
            <Card.Root boxShadow="lg">
              <Card.Header>
                <Heading size="lg">Información de tu Cita</Heading>
              </Card.Header>
              <Card.Body>
                <VStack align="stretch" gap={4}>
                  <HStack justify="space-between">
                    <Text fontWeight="bold">Estado:</Text>
                    <Badge colorScheme={getEstadoColor(citaBuscada.id_estado_cita)}>
                      {getEstadoNombre(citaBuscada.id_estado_cita)}
                    </Badge>
                  </HStack>

                  <HStack justify="space-between">
                    <Text fontWeight="bold">Fecha:</Text>
                    <Text>{citaBuscada.fecha_cita}</Text>
                  </HStack>

                  <HStack justify="space-between">
                    <Text fontWeight="bold">Hora:</Text>
                    <Text>
                      {citaBuscada.hora_inicio} - {citaBuscada.hora_fin}
                    </Text>
                  </HStack>

                  <HStack justify="space-between">
                    <Text fontWeight="bold">Código:</Text>
                    <Text fontFamily="mono">{citaBuscada.codigo_confirmacion}</Text>
                  </HStack>

                  {citaBuscada.motivo_consulta && (
                    <Box>
                      <Text fontWeight="bold" mb={1}>
                        Motivo de Consulta:
                      </Text>
                      <Text color="gray.600">{citaBuscada.motivo_consulta}</Text>
                    </Box>
                  )}

                  {/* Advertencia si está cancelada */}
                  {citaBuscada.id_estado_cita === 5 && (
                    <Alert.Root status="error">
                      <Alert.Indicator />
                      <Alert.Title>Esta cita ha sido cancelada</Alert.Title>
                    </Alert.Root>
                  )}

                  {/* Botones de Acción */}
                  {citaBuscada.id_estado_cita !== 5 && citaBuscada.id_estado_cita !== 3 && (
                    <HStack gap={3} pt={4}>
                      {/* Botón Reagendar */}
                      <DialogRoot>
                        <DialogTrigger asChild>
                          <Button
                            bg="blue.500"
                            color="white"
                            _hover={{ bg: "blue.600", transform: "translateY(-2px)", shadow: "lg" }}
                            flex={1}
                            onClick={() => setReagendando(true)}
                            boxShadow="sm"
                          >
                            Reagendar
                          </Button>
                        </DialogTrigger>

                        <DialogContent>
                          <DialogHeader>
                            <DialogTitle>Reagendar Cita</DialogTitle>
                          </DialogHeader>

                          <DialogBody>
                            <VStack gap={4}>
                              <Field label="Nueva Fecha" required w="full">
                                <Input
                                  type="date"
                                  value={nuevaFecha}
                                  onChange={(e) => setNuevaFecha(e.target.value)}
                                  min={new Date().toISOString().split("T")[0]}
                                />
                              </Field>

                              <Field label="Nueva Hora" required w="full">
                                <Grid templateColumns="repeat(4, 1fr)" gap={2}>
                                  {generarHorarios().map((hora) => (
                                    <Button
                                      key={hora}
                                      onClick={() => setNuevaHora(hora)}
                                      variant={nuevaHora === hora ? "solid" : "outline"}
                                      colorScheme={nuevaHora === hora ? "teal" : "gray"}
                                      size="sm"
                                    >
                                      {hora}
                                    </Button>
                                  ))}
                                </Grid>
                              </Field>
                            </VStack>
                          </DialogBody>

                          <DialogFooter>
                            <DialogActionTrigger asChild>
                              <Button
                                variant="outline"
                                borderColor="gray.300"
                                color="gray.700"
                                _hover={{ bg: "gray.50" }}
                              >
                                Cancelar
                              </Button>
                            </DialogActionTrigger>
                            <Button
                              bg="blue.500"
                              color="white"
                              _hover={{ bg: "blue.600" }}
                              onClick={handleReagendar}
                              loading={reagendarMutation.isPending}
                            >
                              Confirmar Reagendamiento
                            </Button>
                          </DialogFooter>
                        </DialogContent>
                      </DialogRoot>

                      {/* Botón Cancelar */}
                      <DialogRoot>
                        <DialogTrigger asChild>
                          <Button
                            borderWidth="2px"
                            borderColor="blue.500"
                            color="blue.600"
                            bg="white"
                            _hover={{ bg: "blue.50", borderColor: "blue.600", transform: "translateY(-2px)", shadow: "lg" }}
                            flex={1}
                            boxShadow="sm"
                          >
                            Cancelar Cita
                          </Button>
                        </DialogTrigger>

                        <DialogContent>
                          <DialogHeader>
                            <DialogTitle>¿Cancelar Cita?</DialogTitle>
                          </DialogHeader>

                          <DialogBody>
                            <Text>
                              ¿Estás seguro que deseas cancelar tu cita? Esta acción no se
                              puede deshacer.
                            </Text>
                          </DialogBody>

                          <DialogFooter>
                            <DialogActionTrigger asChild>
                              <Button
                                variant="outline"
                                borderColor="gray.300"
                                color="gray.700"
                                _hover={{ bg: "gray.50" }}
                              >
                                No, mantener cita
                              </Button>
                            </DialogActionTrigger>
                            <Button
                              bg="red.500"
                              color="white"
                              _hover={{ bg: "red.600" }}
                              onClick={handleCancelar}
                              loading={cancelarMutation.isPending}
                            >
                              Sí, cancelar
                            </Button>
                          </DialogFooter>
                        </DialogContent>
                      </DialogRoot>
                    </HStack>
                  )}
                </VStack>
              </Card.Body>
            </Card.Root>
          )}
        </VStack>
      </Container>

      <LandingFooter />
    </Box>
  )
}
