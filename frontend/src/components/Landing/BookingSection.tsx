import { Box, Container, Heading, Text, VStack, SimpleGrid, Icon } from "@chakra-ui/react"
import { FaInfoCircle, FaMapMarkerAlt } from "react-icons/fa"
import { useInView } from "react-intersection-observer"

export default function BookingSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })

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
          </VStack>

          <Box
            w="full"
            maxW="100%"
            mx="auto"
            opacity={inView ? 1 : 0}
            transform={inView ? "translateY(0)" : "translateY(30px)"}
            transition="all 0.8s 0.2s"
            boxShadow="xl"
            borderRadius="2xl"
            overflow="hidden"
            bg="white"
          >
            <Box
              as="iframe"
              src="https://calendar.google.com/calendar/appointments/schedules/AcZssZ3NH_ZzHCI5OI5AbLXjtpPFslDpY1VG2v-5zOX_TYts3lYZ0pzI2r9fpwz68zrH4fcZcFnJlFEu?gv=true"
              w="full"
              h="600px"
              border="0"
              loading="lazy"
              title="Calendario de Citas Conectemos Chile"
            />
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
