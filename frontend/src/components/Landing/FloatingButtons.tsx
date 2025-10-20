import { Box, Link, Flex, Text } from "@chakra-ui/react"
import { FaWhatsapp, FaCalendarAlt } from "react-icons/fa"

export default function FloatingButtons() {
  return (
    <Box
      position="fixed"
      bottom={8}
      right={8}
      zIndex={999}
      display="flex"
      flexDirection="column"
      gap={4}
    >
      {/* WhatsApp Button */}
      <Link
        href="https://wa.me/56921991963?text=Hola,%20me%20gustaría%20agendar%20una%20consulta%20en%20Conectemos%20Chile"
        target="_blank"
        rel="noopener noreferrer"
        position="relative"
        _hover={{ textDecoration: "none" }}
      >
        <Flex
          align="center"
          justify="center"
          w="60px"
          h="60px"
          bg="#25D366"
          color="white"
          borderRadius="full"
          boxShadow="0 4px 20px rgba(37, 211, 102, 0.5)"
          _hover={{
            bg: "#20BA5A",
            transform: "scale(1.1)",
          }}
          transition="all 0.3s"
          cursor="pointer"
        >
          <FaWhatsapp size={28} />
        </Flex>
        <Box
          position="absolute"
          right="70px"
          top="50%"
          transform="translateY(-50%)"
          bg="white"
          px={4}
          py={2}
          borderRadius="lg"
          boxShadow="lg"
          whiteSpace="nowrap"
          opacity={0}
          pointerEvents="none"
          _groupHover={{ opacity: 1 }}
          transition="opacity 0.3s"
        >
          <Text fontSize="sm" fontWeight="600" color="gray.800">
            ¿Necesitas ayuda? ¡Agenda tu consulta!
          </Text>
        </Box>
      </Link>

      {/* Calendar Button */}
      <Link
        href="https://calendar.google.com/calendar/appointments/schedules/AcZssZ3NH_ZzHCI5OI5AbLXjtpPFslDpY1VG2v-5zOX_TYts3lYZ0pzI2r9fpwz68zrH4fcZcFnJlFEu?gv=true"
        target="_blank"
        rel="noopener noreferrer"
        position="relative"
        _hover={{ textDecoration: "none" }}
      >
        <Flex
          align="center"
          justify="center"
          w="60px"
          h="60px"
          bg="#4285F4"
          color="white"
          borderRadius="full"
          boxShadow="0 4px 20px rgba(66, 133, 244, 0.5)"
          _hover={{
            bg: "#3264C8",
            transform: "scale(1.1)",
          }}
          transition="all 0.3s"
          cursor="pointer"
        >
          <FaCalendarAlt size={24} />
        </Flex>
        <Box
          position="absolute"
          right="70px"
          top="50%"
          transform="translateY(-50%)"
          bg="white"
          px={4}
          py={2}
          borderRadius="lg"
          boxShadow="lg"
          whiteSpace="nowrap"
          opacity={0}
          pointerEvents="none"
          _groupHover={{ opacity: 1 }}
          transition="opacity 0.3s"
        >
          <Text fontSize="sm" fontWeight="600" color="gray.800">
            Agenda con nosotros! 🙋🏻‍♂️
          </Text>
        </Box>
      </Link>
    </Box>
  )
}
