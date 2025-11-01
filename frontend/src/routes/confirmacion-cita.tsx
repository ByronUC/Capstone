import { createFileRoute, useNavigate } from "@tanstack/react-router"
import {
  Box,
  Container,
  Heading,
  VStack,
  Text,
  Button,
  Card,
  HStack,
  Icon,
} from "@chakra-ui/react"
import { FiCheckCircle, FiCopy } from "react-icons/fi"
import { toaster } from "../components/ui/toaster"
import LandingNavbar from "../components/Landing/LandingNavbar"
import LandingFooter from "../components/Landing/LandingFooter"

export const Route = createFileRoute("/confirmacion-cita")({
  component: ConfirmacionCitaPage,
  validateSearch: (search: Record<string, unknown>) => ({
    codigo: (search.codigo as string) || "",
  }),
})

function ConfirmacionCitaPage() {
  const navigate = useNavigate()
  const { codigo } = Route.useSearch()

  const copiarCodigo = () => {
    navigator.clipboard.writeText(codigo)
    toaster.create({
      title: "Código copiado",
      description: "El código se ha copiado al portapapeles",
      type: "success",
    })
  }

  return (
    <Box minH="100vh" bg="gray.50">
      <LandingNavbar />

      <Container maxW="container.md" py={12}>
        <VStack gap={6} align="stretch">
          {/* Success Icon */}
          <Box textAlign="center">
            <Icon fontSize="5xl" color="blue.500">
              <FiCheckCircle />
            </Icon>
          </Box>

          {/* Main Card */}
          <Card.Root boxShadow="lg">
            <Card.Body p={6}>
              <VStack gap={5} align="stretch">
                <Heading size="lg" textAlign="center" color="blue.600">
                  ¡Cita Reservada Exitosamente!
                </Heading>

                <Text textAlign="center" fontSize="md" color="gray.600">
                  Tu solicitud de cita ha sido recibida y está{" "}
                  <strong>pendiente de confirmación</strong> por nuestro equipo de
                  recepción.
                </Text>

                {/* Código de Confirmación */}
                <Box
                  p={4}
                  bg="blue.50"
                  borderRadius="lg"
                  borderWidth="2px"
                  borderColor="blue.200"
                >
                  <VStack gap={2}>
                    <Text fontWeight="semibold" fontSize="sm" color="gray.700">
                      Tu Código de Confirmación:
                    </Text>
                    <HStack gap={2}>
                      <Text
                        fontSize="2xl"
                        fontWeight="bold"
                        color="blue.600"
                        letterSpacing="wider"
                        fontFamily="mono"
                      >
                        {codigo}
                      </Text>
                      <Button
                        size="sm"
                        onClick={copiarCodigo}
                        variant="ghost"
                        colorScheme="blue"
                      >
                        <FiCopy />
                      </Button>
                    </HStack>
                    <Text fontSize="xs" color="gray.600" textAlign="center">
                      Guarda este código para reagendar o cancelar tu cita
                    </Text>
                  </VStack>
                </Box>

                {/* Información */}
                <Box p={3} bg="white" borderRadius="md" borderWidth="1px" borderColor="gray.200">
                  <VStack align="start" gap={1.5}>
                    <Text fontWeight="semibold" color="gray.700" fontSize="sm">
                      📧 Te hemos enviado un email con:
                    </Text>
                    <Text fontSize="xs" color="gray.600">
                      • Tu código de confirmación
                    </Text>
                    <Text fontSize="xs" color="gray.600">
                      • Detalles de tu cita
                    </Text>
                    <Text fontSize="xs" color="gray.600">
                      • Instrucciones para reagendar o cancelar
                    </Text>
                  </VStack>
                </Box>

                {/* Próximos Pasos */}
                <Box p={3} bg="white" borderRadius="md" borderWidth="1px" borderColor="gray.200">
                  <VStack align="start" gap={1.5}>
                    <Text fontWeight="semibold" color="gray.700" fontSize="sm">
                      ⏳ Próximos Pasos:
                    </Text>
                    <Text fontSize="xs" color="gray.600">
                      1. Nuestro equipo de recepción revisará tu solicitud
                    </Text>
                    <Text fontSize="xs" color="gray.600">
                      2. Recibirás un email de confirmación final
                    </Text>
                    <Text fontSize="xs" color="gray.600">
                      3. Tu cita aparecerá en Google Calendar (si confirmada)
                    </Text>
                  </VStack>
                </Box>

                {/* Botones de Acción */}
                <VStack gap={2}>
                  <Button
                    colorScheme="blue"
                    size="md"
                    w="full"
                    onClick={() => navigate({ to: "/gestionar-cita" })}
                  >
                    Gestionar mi Cita
                  </Button>
                  <Button
                    variant="outline"
                    colorScheme="gray"
                    size="md"
                    w="full"
                    onClick={() => navigate({ to: "/" })}
                  >
                    Volver al Inicio
                  </Button>
                </VStack>
              </VStack>
            </Card.Body>
          </Card.Root>
        </VStack>
      </Container>

      <LandingFooter />
    </Box>
  )
}
