import { createFileRoute } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  Box,
  Container,
  Heading,
  Table,
  Badge,
  Button,
  Spinner,
  Alert,
  HStack,
  Text,
} from "@chakra-ui/react"
import { FiCheck, FiX, FiRefreshCw } from "react-icons/fi"
import { toaster } from "../../components/ui/toaster"
import {
  DialogActionTrigger,
  DialogBody,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
} from "../../components/ui/dialog"
import { BookingService, type Cita } from "../../client/booking"

export const Route = createFileRoute("/_layout/citas-pendientes")({
  component: CitasPendientesPage,
})

function CitasPendientesPage() {
  const queryClient = useQueryClient()

  // Query para obtener citas pendientes
  const {
    data: citasData,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ["citas-pendientes"],
    queryFn: () => BookingService.getCitasPendientes(0, 100),
    refetchInterval: 30000, // Refetch cada 30 segundos
  })

  // Mutation para confirmar cita
  const confirmarMutation = useMutation({
    mutationFn: (idCita: number) => BookingService.confirmarCita(idCita),
    onSuccess: () => {
      toaster.create({
        title: "Cita confirmada",
        description: "La cita ha sido confirmada exitosamente",
        type: "success",
      })
      queryClient.invalidateQueries({ queryKey: ["citas-pendientes"] })
    },
    onError: (error: Error) => {
      toaster.create({
        title: "Error al confirmar",
        description: error.message,
        type: "error",
      })
    },
  })

  const formatFecha = (fecha: string) => {
    const fechaObj = new Date(fecha + "T12:00:00")
    return fechaObj.toLocaleDateString("es-CL", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  const formatHora = (hora: string) => {
    return hora.substring(0, 5)
  }

  if (isLoading) {
    return (
      <Container maxW="container.xl" py={10}>
        <Box textAlign="center" py={20}>
          <Spinner size="xl" />
          <Text mt={4}>Cargando citas pendientes...</Text>
        </Box>
      </Container>
    )
  }

  return (
    <Container maxW="container.xl" py={10}>
      <Box>
        {/* Header */}
        <HStack justify="space-between" mb={6}>
          <Heading size="xl">Citas Pendientes de Confirmación</Heading>
          <Button
            onClick={() => refetch()}
            variant="outline"
            colorScheme="teal"
            leftIcon={<FiRefreshCw />}
          >
            Actualizar
          </Button>
        </HStack>

        {/* Badge con contador */}
        <HStack mb={4}>
          <Badge colorScheme="yellow" fontSize="lg" px={3} py={1}>
            {citasData?.count || 0} citas pendientes
          </Badge>
        </HStack>

        {/* Tabla de Citas */}
        {citasData && citasData.count > 0 ? (
          <Box overflowX="auto">
            <Table.Root size="lg">
              <Table.Header>
                <Table.Row>
                  <Table.ColumnHeader>Fecha</Table.ColumnHeader>
                  <Table.ColumnHeader>Hora</Table.ColumnHeader>
                  <Table.ColumnHeader>ID Paciente</Table.ColumnHeader>
                  <Table.ColumnHeader>ID Psicólogo</Table.ColumnHeader>
                  <Table.ColumnHeader>Servicio</Table.ColumnHeader>
                  <Table.ColumnHeader>Código</Table.ColumnHeader>
                  <Table.ColumnHeader>Motivo</Table.ColumnHeader>
                  <Table.ColumnHeader textAlign="center">Acciones</Table.ColumnHeader>
                </Table.Row>
              </Table.Header>
              <Table.Body>
                {citasData.data.map((cita: Cita) => (
                  <Table.Row key={cita.id_cita}>
                    <Table.Cell fontWeight="medium">
                      {formatFecha(cita.fecha_cita)}
                    </Table.Cell>
                    <Table.Cell>
                      {formatHora(cita.hora_inicio)} - {formatHora(cita.hora_fin)}
                    </Table.Cell>
                    <Table.Cell>#{cita.id_paciente}</Table.Cell>
                    <Table.Cell>#{cita.id_psicologo}</Table.Cell>
                    <Table.Cell>#{cita.id_servicio}</Table.Cell>
                    <Table.Cell>
                      <Badge colorScheme="purple" fontFamily="mono">
                        {cita.codigo_confirmacion}
                      </Badge>
                    </Table.Cell>
                    <Table.Cell maxW="200px" isTruncated>
                      {cita.motivo_consulta || "-"}
                    </Table.Cell>
                    <Table.Cell>
                      <HStack justify="center" gap={2}>
                        {/* Botón Confirmar */}
                        <DialogRoot>
                          <DialogTrigger asChild>
                            <Button colorScheme="green" size="sm" leftIcon={<FiCheck />}>
                              Confirmar
                            </Button>
                          </DialogTrigger>

                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle>Confirmar Cita</DialogTitle>
                            </DialogHeader>

                            <DialogBody>
                              <Text>
                                ¿Confirmar la cita para el {formatFecha(cita.fecha_cita)} a
                                las {formatHora(cita.hora_inicio)}?
                              </Text>
                              <Box mt={4} p={3} bg="gray.100" borderRadius="md">
                                <Text fontSize="sm">
                                  <strong>Código:</strong> {cita.codigo_confirmacion}
                                </Text>
                                <Text fontSize="sm">
                                  <strong>Paciente:</strong> #{cita.id_paciente}
                                </Text>
                                <Text fontSize="sm">
                                  <strong>Psicólogo:</strong> #{cita.id_psicologo}
                                </Text>
                              </Box>
                            </DialogBody>

                            <DialogFooter>
                              <DialogActionTrigger asChild>
                                <Button variant="outline">Cancelar</Button>
                              </DialogActionTrigger>
                              <Button
                                colorScheme="green"
                                onClick={() => confirmarMutation.mutate(cita.id_cita!)}
                                loading={confirmarMutation.isPending}
                              >
                                Sí, Confirmar
                              </Button>
                            </DialogFooter>
                          </DialogContent>
                        </DialogRoot>

                        {/* Botón Rechazar (Opcional - por implementar) */}
                        <Button
                          colorScheme="red"
                          variant="outline"
                          size="sm"
                          leftIcon={<FiX />}
                          isDisabled
                        >
                          Rechazar
                        </Button>
                      </HStack>
                    </Table.Cell>
                  </Table.Row>
                ))}
              </Table.Body>
            </Table.Root>
          </Box>
        ) : (
          <Alert.Root status="info">
            <Alert.Indicator />
            <Alert.Title>No hay citas pendientes</Alert.Title>
            <Alert.Description>
              Todas las citas han sido confirmadas o no hay solicitudes nuevas.
            </Alert.Description>
          </Alert.Root>
        )}
      </Box>
    </Container>
  )
}
