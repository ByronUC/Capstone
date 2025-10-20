import { Box, Container, Heading, Text, VStack, Grid, HStack, Flex } from "@chakra-ui/react"
import { useInView } from "react-intersection-observer"
import { FaStar, FaUser } from "react-icons/fa"
import { useEffect } from "react"

// Testimonios de ejemplo - Reemplazar con datos reales o widget de Elfsight
const testimonials = [
  {
    name: "María González",
    avatar: "MG",
    rating: 5,
    date: "Hace 2 semanas",
    comment: "Excelente atención profesional. El equipo es muy comprometido y me han ayudado mucho en mi proceso terapéutico. Totalmente recomendado.",
  },
  {
    name: "Carlos Ramírez",
    avatar: "CR",
    rating: 5,
    date: "Hace 1 mes",
    comment: "La mejor decisión que pude tomar. Los profesionales son muy capacitados y el ambiente es acogedor. Me siento muy bien atendido.",
  },
  {
    name: "Ana Martínez",
    avatar: "AM",
    rating: 5,
    date: "Hace 3 semanas",
    comment: "Muy profesionales y empáticos. Han sido fundamentales en mi proceso de recuperación. Gracias por todo el apoyo brindado.",
  },
]

export default function TestimonialsSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })

  useEffect(() => {
    // Script para cargar el widget de Elfsight si está configurado
    // Descomentar y agregar tu widget ID cuando tengas tu cuenta de Elfsight
    /*
    const script = document.createElement('script')
    script.src = 'https://static.elfsight.com/platform/platform.js'
    script.defer = true
    document.body.appendChild(script)
    return () => {
      document.body.removeChild(script)
    }
    */
  }, [])

  return (
    <Box
      id="testimonials"
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
              Lo Que Dicen Nuestros Pacientes
            </Heading>
            <Text fontSize={{ base: "lg", md: "xl" }} color="gray.600" maxW="800px">
              Testimonios reales de personas que han confiado en nosotros
            </Text>
          </VStack>

          {/* Widget de Elfsight - Descomentar cuando tengas tu widget ID */}
          {/* <Box w="full" className="elfsight-app-YOUR-WIDGET-ID"></Box> */}

          {/* Testimonios de ejemplo - Comentar o eliminar cuando uses el widget de Elfsight */}
          <Grid
            templateColumns={{ base: "1fr", md: "repeat(2, 1fr)", lg: "repeat(3, 1fr)" }}
            gap={6}
            w="full"
            opacity={inView ? 1 : 0}
            transform={inView ? "translateY(0)" : "translateY(30px)"}
            transition="all 0.8s 0.2s"
          >
            {testimonials.map((testimonial, index) => (
              <Box
                key={index}
                bg="white"
                p={6}
                borderRadius="xl"
                boxShadow="md"
                _hover={{ boxShadow: "lg", transform: "translateY(-4px)" }}
                transition="all 0.3s"
              >
                <VStack align="stretch" gap={4}>
                  <HStack justify="space-between">
                    <HStack gap={3}>
                      <Flex
                        width="48px"
                        height="48px"
                        borderRadius="full"
                        bg="#FFA726"
                        color="white"
                        fontWeight="600"
                        fontSize="lg"
                        alignItems="center"
                        justifyContent="center"
                      >
                        <FaUser size={20} />
                      </Flex>
                      <Box>
                        <Text fontWeight="600" color="gray.800">
                          {testimonial.name}
                        </Text>
                        <Text fontSize="xs" color="gray.500">
                          {testimonial.date}
                        </Text>
                      </Box>
                    </HStack>
                  </HStack>
                  <HStack gap={1}>
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <FaStar key={i} color="#FFA726" size={16} />
                    ))}
                  </HStack>
                  <Text fontSize="sm" color="gray.600" lineHeight="1.6">
                    {testimonial.comment}
                  </Text>
                </VStack>
              </Box>
            ))}
          </Grid>

          <Text fontSize="sm" color="gray.500" textAlign="center" maxW="600px">
            Para integrar tu widget de Google Reviews real, registra tu widget en{" "}
            <Text as="span" color="#FFA726" fontWeight="600">
              Elfsight.com
            </Text>{" "}
            y reemplaza los testimonios de ejemplo con el código del widget.
          </Text>
        </VStack>
      </Container>
    </Box>
  )
}
