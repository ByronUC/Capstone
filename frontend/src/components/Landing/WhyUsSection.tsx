import { Box, Container, Heading, Text, VStack, SimpleGrid, Icon } from "@chakra-ui/react"
import { FaCertificate, FaClock, FaHeart, FaFileInvoiceDollar } from "react-icons/fa"
import { useInView } from "react-intersection-observer"

export default function WhyUsSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })

  const reasons = [
    {
      icon: FaCertificate,
      title: "Profesionales Certificados",
      description: "Nuestro equipo cuenta con certificaciones oficiales y formación constante para entregarte una atención confiable y de calidad."
    },
    {
      icon: FaClock,
      title: "Disponibilidad en Modalidad y Horarios",
      description: "Elige entre atención presencial u online, con alternativas en horario diurno y vespertino para mayor comodidad."
    },
    {
      icon: FaHeart,
      title: "Enfoque Personalizado",
      description: "Diseñamos un plan terapéutico adaptado a tus necesidades y objetivos, acompañándote en cada etapa de tu proceso."
    },
    {
      icon: FaFileInvoiceDollar,
      title: "Boletas Reembolsables",
      description: "Todas nuestras boletas son reembolsables con cualquier Isapre y/o seguro complementario, facilitando el acceso a tu terapia."
    }
  ]

  return (
    <Box
      id="why-us"
      py={{ base: 16, md: 24 }}
      bg="white"
      position="relative"
      ref={ref}
    >
      {/* Decorative elements */}
      <Box position="absolute" bottom="10%" right="5%" w="200px" h="200px" borderRadius="50%" bg="rgba(255, 167, 38, 0.05)" />

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
              Por Qué Elegirnos
            </Heading>
            <Text fontSize={{ base: "lg", md: "xl" }} color="gray.600" maxW="800px">
              Lo que nos diferencia
            </Text>
          </VStack>

          <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} gap={8} w="full">
            {reasons.map((reason, index) => (
              <Box
                key={index}
                bg="white"
                p={8}
                borderRadius="2xl"
                boxShadow="lg"
                textAlign="center"
                opacity={inView ? 1 : 0}
                transform={inView ? "translateY(0)" : "translateY(30px)"}
                transition={`all 0.8s ${0.2 + index * 0.1}s`}
                _hover={{
                  transform: "translateY(-8px)",
                  boxShadow: "2xl",
                  borderColor: "#4285F4",
                  borderWidth: "2px"
                }}
                borderWidth="2px"
                borderColor="transparent"
              >
                <VStack gap={4}>
                  <Box
                    bg="rgba(66, 133, 244, 0.1)"
                    p={4}
                    borderRadius="full"
                    display="inline-flex"
                  >
                    <Icon as={reason.icon} fontSize="3xl" color="#4285F4" />
                  </Box>
                  <Heading as="h3" fontSize="xl" color="gray.800">
                    {reason.title}
                  </Heading>
                  <Text fontSize="md" color="gray.700" lineHeight="1.8">
                    {reason.description}
                  </Text>
                </VStack>
              </Box>
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  )
}
